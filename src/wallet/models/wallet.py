from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from wallet.models.currency import Currency


User = get_user_model()


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

    address = models.CharField(_("address"), max_length=100, db_index=True)
    color = models.CharField(_("color"), max_length=7, null=True, blank=True)
    created = models.DateTimeField(_("created"), null=True, blank=True)
    updated = models.DateTimeField(_("updated"), null=True, blank=True)

    initialized = models.BooleanField(_("initialized"), default=False)
    updated_from_2nd_svr = models.DateTimeField(_("updated_from_2nd_svr"), null=True, blank=True)
    transactions_detail = models.TextField(_("Transactions update detail"), default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['currency', 'address'],
                name="unique_net_address"
            )
        ]
        verbose_name = _("wallet")
        verbose_name_plural = _("wallets")

    def __str__(self):
        return f"{self.user.email}"
