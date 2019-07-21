from django.contrib import admin

from account.models.policy import PrivacyPolicy


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    list_display_links = [
        'name',
    ]
    search_fields = [
        'name'
    ]
