from django.contrib import admin
from django.contrib.auth import get_user_model

from account.models.account import Account


User = get_user_model()


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [
        'user',
    ]
    list_display_links = [
        'user',
    ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email', ]
    list_display = (
        'id',
        'email',
    )
