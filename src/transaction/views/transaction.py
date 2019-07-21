import datetime as dt
from itertools import zip_longest

from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Sum, Min, Q, Max
from django.utils import dateparse
from django.conf import settings

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from Citadel.helpers import define_scale, get_second, make_consistent
from transaction.models import Transaction
from wallet.models import Currency, Rate

from transaction.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all().prefetch_related(
        'wallet__currency'
    ).order_by('-committed')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = (
        'wallet__currency__code',
        'wallet',
    )
    ordering_fields = (
        'pk',
        'currency',
        'address_from',
        'address_to',
        'mission',
        'volume',
        'commission',
        'committed',
    )
    missions_reward = {
        Transaction.MISSION_PAYMENT: True,
        Transaction.MISSION_APPROVED_PAYMENT: True,
    }
    missions_balance = {
        Transaction.MISSION_PAYMENT: True,
        Transaction.MISSION_APPROVED_PAYMENT: True,
        Transaction.MISSION_SUPPLEMENT: True,
        Transaction.MISSION_CONCLUSION: False
    }

    def get_queryset(self):
        qs = super(TransactionViewSet, self).get_queryset()
        qs = qs.filter(wallet__user=self.request.user)

        return qs

    def get_missions(self, is_income=True, balance=False):
        mission = self.missions_balance if balance else self.missions_reward
        return [code for code, income in mission.items() if income == is_income]

    def get_chart_data(self, currency, date_from=None, date_to=None, add_balance=False, scale=None):
        scale = scale or define_scale(date_from, date_to, add_balance)
        rates = Rate.get_actual_rates(currency)

        inc_codes = self.get_missions(is_income=True, balance=add_balance)
        dec_codes = self.get_missions(is_income=False, balance=add_balance)
        qs = self.get_queryset().datetimes(
            field_name='committed',
            kind=scale,
            order='ASC'
        ).filter(
            wallet__currency=currency
        ).annotate(
            sum_inc=Sum('volume', filter=Q(mission__in=inc_codes)),
            sum_dec=Sum('volume', filter=Q(mission__in=dec_codes)),
        )

        # Set starting volume value
        volume = 0

        no_transaction_after_date_filtration = False
        initial_date = None

        if date_from and date_to:
            qs_filtered_by_date = qs.filter(
                committed__gte=date_from,
                committed__lte=date_to
            )

            if qs and not qs_filtered_by_date:
                # После фильтраций транзакций нет
                # Поэтому первое значение для графика нужно создать искуственно
                no_transaction_after_date_filtration = True
                initial_date = date_from
            else:
                qs = qs_filtered_by_date

            # Get volume sum before 'date_from' date
            start_sums = self.get_queryset().filter(
                wallet__currency=currency,
                committed__lt=date_from,
            ).aggregate(
                sum_inc=Sum('volume', filter=Q(mission__in=inc_codes)),
                sum_dec=Sum('volume', filter=Q(mission__in=dec_codes))
            )
            sum_inc = start_sums['sum_inc'] if start_sums['sum_inc'] else 0
            sum_dec = start_sums['sum_dec'] if start_sums['sum_dec'] else 0
            volume = sum_inc - sum_dec

        if no_transaction_after_date_filtration:
            chart_data = [
                {
                    'datetimefield': initial_date,
                    'sum_inc': 0,
                    'sum_dec': 0,
                }
            ]
        else:
            chart_data = list(
                qs.values(
                    'datetimefield',
                    'sum_inc',
                    'sum_dec'
                )
            )

        chart_data_accum = []
        consistent_data = make_consistent(
            orig_list=chart_data,
            target='datetimefield',
            max_value=date_to,
            delta=get_second(scale)
        )
        for point, appended in consistent_data:
            if not appended:
                volume_inc = point['sum_inc'] if point['sum_inc'] else 0
                volume_dec = point['sum_dec'] if point['sum_dec'] else 0

                delta = volume_inc - volume_dec
                volume += delta
            else:
                delta = 0

            # Для стейкинга показываем, сколько заработал за конкретный день, а не накопленную сумму
            amount = volume if add_balance else delta
            chart_data_accum.append({
                'datetimefield': point['datetimefield'],
                'volume': amount,
                'usd': amount * rates['usd'],
                'btc': amount * rates['btc']
            })
        return chart_data_accum

    def get_overall_charts_data(self, charts_data):
        # Списки могут быть разной длины (н-р, один список начинается со 2го января, а вторйо - с 3его)
        # Поэтому надо их выровнить слева. Делаю это с помощью сочетания zip_longest и reverse

        # Для выравнивания слева берутся нулевые значения,
        # т.к. пользователь не имел данный токен в данную дату
        fill_value = {
            'btc': 0,
            'usd': 0,
            'datetimefield': None,
        }

        charts_data = [reversed(chart_data) for chart_data in charts_data if chart_data]
        overall_data = [
            {
                'volume': None,
                'btc': sum(day_data['btc'] for day_data in zipped_day_data),
                'usd': sum(day_data['usd'] for day_data in zipped_day_data),
                'datetimefield': next(
                    day_data['datetimefield'] for day_data in zipped_day_data
                    if day_data['datetimefield'] is not None
                )
            }
            for zipped_day_data in zip_longest(*charts_data, fillvalue=fill_value)
        ]
        return list(reversed(overall_data))

    @action(detail=False, methods=['get'])
    def chart(self, request):
        currency_code = request.GET.get('currency', None)
        date_from = request.GET.get('chart_date_from', None)
        date_to = request.GET.get('chart_date_to', None)
        add_balance = request.GET.get('add_balance', 'false') == 'true'

        # Get currency
        if currency_code:
            currencies = Currency.init_currencies.filter(code=currency_code)
            if not currencies:
                raise NotFound(f"currency code: {currency_code}")
        else:
            currencies = Currency.init_currencies.all()

        # Define date filter
        if date_from:
            date_from = dateparse.parse_datetime(date_from)
        else:
            date_from = dt.datetime.today() - dt.timedelta(weeks=4)

        if date_to:
            date_to = dateparse.parse_datetime(date_to)
        else:
            date_to = dt.datetime.now()

        if not (date_to and date_from):
            raise ValidationError("no valid dates")

        # ToDo: optimize this!
        charts_data = [
            self.get_chart_data(currency, date_from, date_to, add_balance)
            for currency in currencies
        ]
        if len(charts_data) == 1:
            return Response(charts_data[0])
        return Response(self.get_overall_charts_data(charts_data))

    @action(url_path='chart-below', detail=False, methods=['get'])
    def chart_below(self, request):
        currency_code = request.GET.get('currency', None)
        add_balance = request.GET.get('add_balance', 'false') == 'true'

        date_from = None
        date_to = None
        # Get currency
        if currency_code:
            currencies = Currency.init_currencies.filter(code=currency_code)
            if not currencies:
                raise NotFound(f"currency code: {currency_code}")
        else:
            currencies = list(
                Currency.init_currencies
                        .annotate(max_date=Max('wallet__transactions__committed'))
                        .annotate(min_date=Min('wallet__transactions__committed'))
            )
            date_from = min(currency.min_date for currency in currencies if currency.min_date)
            date_to = max(currency.max_date for currency in currencies if currency.max_date)

        # ToDo: optimize this!
        charts_data = [
            self.get_chart_data(currency, date_from, date_to, add_balance, scale='week')
            for currency in currencies
        ]

        if len(charts_data) == 1:
            return Response(charts_data[0])
        a = self.get_overall_charts_data(charts_data)
        return Response(self.get_overall_charts_data(charts_data))

    @action(detail=False, methods=['get'])
    def reward(self, request):
        date_from = request.GET.get('chart_date_from', None)
        date_to = request.GET.get('chart_date_to', None)
        add_balance = request.GET.get('add_balance', 'false') == 'true'

        dates = None
        if date_from and date_to:
            dates = {
                'from': date_from,
                'to': date_to
            }

        missions_inc = [Transaction.MISSION_PAYMENT, Transaction.MISSION_APPROVED_PAYMENT]
        missions_dec = []
        if add_balance:
            missions_inc.append(Transaction.MISSION_SUPPLEMENT)
            missions_dec.append(Transaction.MISSION_CONCLUSION)

        qs = Currency.init_currencies.filter(
            wallet__user=request.user,
        ).annotate(
            sum_inc=Sum('wallet__transactions__volume', filter=Q(
                wallet__transactions__mission__in=missions_inc
            )),
            sum_dec=Sum('wallet__transactions__volume', filter=Q(
                wallet__transactions__mission__in=missions_dec
            )),
        )
        if dates:
            qs = qs.filter(
                wallet__transactions__committed__gte=dates['from'],
                wallet__transactions__committed__lte=dates['to']
            )

        currencies_reward = {}
        for currency in qs.values('code', 'sum_inc', 'sum_dec'):
            rate = Rate.get_rate_by_code(currency['code'])
            sum_inc = currency['sum_inc'] if currency['sum_inc'] else 0
            sum_dec = currency['sum_dec'] if currency['sum_dec'] else 0
            total = sum_inc - sum_dec
            currencies_reward[currency['code']] = {
                'sum_volume': total,
                'sum_volume_usd': total * rate['usd'],
                'sum_volume_btc': total * rate['btc']
            }

        total_reward = {}
        for c in currencies_reward.values():
            for k,v in c.items():
                try:
                    total_reward[k] += v
                except:
                    total_reward[k] = v

        first_date = self.get_queryset().filter(
            mission__in=[Transaction.MISSION_PAYMENT, Transaction.MISSION_APPROVED_PAYMENT]
        ).aggregate(min=Min('committed')).get('min', None)

        response = {
            'first_payment_date': first_date,
            'total_reward': total_reward,
            'reward': currencies_reward,
        }
        return Response(response)
