from django.contrib import admin

from wallet.models.currency import Currency, Rate, CurrencySocial, CurrencyStatistics


class CurrencySocialInline(admin.TabularInline):
    model = CurrencySocial


class CurrencyStatisticsInline(admin.TabularInline):
    model = CurrencyStatistics


@admin.register(CurrencyStatistics)
class CurrencyStatisticsAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'currency',
        'price_usd',
        'price_btc',
        'price_usd_delta_24',
        'price_btc_delta_24',
    ]
    list_display_links = [
        'pk',
    ]
    search_fields = [
        'currency__name',
    ]


@admin.register(CurrencySocial)
class CurrencySocialAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'url',
        'icon',
        'currency',
    ]
    list_display_links = [
        'pk',
    ]
    search_fields = [
        'name',
        'url',
        'currency__name',
    ]


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'sign',
        'name',
        'code',
        'net',
        'initialized',
        'icon'
    ]
    list_display_links = [
        'pk',
    ]
    search_fields = [
        'name', 'code'
    ]
    inlines = [
        CurrencySocialInline,
        CurrencyStatisticsInline,
    ]


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'currency',
        'usd',
        'btc',
        'datetime'
    ]
    list_display_links = [
        'pk',
    ]
    list_filter = [
        'datetime'
    ]