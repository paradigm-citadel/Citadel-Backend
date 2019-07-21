from django.contrib import admin

from wallet.models.wallet import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'currency',
        'address',
        'created'
    ]
    list_display_links = [
        'user',
    ]
