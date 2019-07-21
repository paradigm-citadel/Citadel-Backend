from django.contrib import admin

from transaction.models.transaction import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'wallet',
        'address_from',
        'address_to',
        'mission',
        'volume',
        'commission',
        'committed'
    ]
    list_display_links = [
        'pk',
    ]
    search_fields = [
        'address_from', 'address_to'
    ]
