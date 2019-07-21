from django.db import models
from django.utils.translation import gettext as _


class CurrencyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class InitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(initialized=True)


class Currency(models.Model):
    name = models.CharField(_("name"), max_length=30)
    description = models.TextField(_("description"), default='')
    sign = models.CharField(_("sign"), max_length=10, default='?')
    code = models.CharField(_("code"), max_length=10, unique=True, db_index=True)
    net = models.CharField(_("net"), max_length=10, default='?')
    initialized = models.BooleanField(_("initialized"), default=False)
    icon = models.ImageField(_("icon"), upload_to='currency', null=True, blank=True)

    objects = CurrencyManager()
    init_currencies = InitManager()

    def __str__(self):
        return f"{self.net}-{self.code}"

    class Meta:
        verbose_name = _("currency")
        verbose_name_plural = _("currencies")


class CurrencySocial(models.Model):
    name = models.CharField("name", max_length=100)
    url = models.URLField("url")
    icon = models.ImageField(_("icon"), upload_to='currency_social', null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='social')

    def __str__(self):
        return f"{self.name}-{self.currency}"

    class Meta:
        verbose_name = _("currency social")
        verbose_name_plural = _("currencies social")


class CurrencyStatistics(models.Model):
    currency = models.OneToOneField(
        Currency,
        on_delete=models.CASCADE,
        related_name='statistics',
        null=True,
        blank=True
    )
    price_usd = models.FloatField(_("price USD"), null=True, blank=True)
    price_btc = models.FloatField(_("price BTC"), null=True, blank=True)
    price_usd_delta_24 = models.FloatField(_("price usd delta 24"), null=True, blank=True)
    price_btc_delta_24 = models.FloatField(_("price btc delta 24"), null=True, blank=True)

    yielded = models.FloatField(_("yielded"), null=True, blank=True)
    market_cap = models.FloatField(_("marketCap"), null=True, blank=True)
    circulating_supply = models.FloatField(_("circulating supply"), null=True, blank=True)
    staking_rate = models.FloatField(_("staking rate"), null=True, blank=True)
    unbonding_period = models.FloatField(_("unbonding period"), null=True, blank=True)

    second_backend_update_datetime = models.DateTimeField(_("second backend update datetime"))
    update_datetime = models.DateTimeField(_("update datetime"), auto_now=True)

    def __str__(self):
        return str(self.currency)

    class Meta:
        verbose_name = _("currency statistics")
        verbose_name_plural = _("currencies statistics")


class Rate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    datetime = models.DateTimeField(_("datetime"), db_index=True)
    usd = models.FloatField(_("USD"), null=True)
    btc = models.FloatField(_("BTC"), null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['currency', 'datetime'],
                name="unique_currency_datetime"
            )
        ]
        verbose_name = _("currency rate")
        verbose_name_plural = _("currencies rates")

    @staticmethod
    def get_actual_rates(currency):
        """ Get closest currency rate for date """
        rate = Rate.objects.filter(
            currency=currency,
            usd__isnull=False,
            btc__isnull=False
        ).order_by('-datetime').first()
        if not rate:
            return None

        result = {
            'usd': rate.usd,
            'btc': rate.btc
        }
        return result

    @staticmethod
    def get_rate_by_code(currency_code):
        """ Get closest currency rate for date """
        rate = Rate.objects.filter(
            currency__code=currency_code,
            usd__isnull=False,
            btc__isnull=False
        ).order_by('-datetime').first()
        if not rate:
            return None

        result = {
            'usd': rate.usd,
            'btc': rate.btc
        }
        return result