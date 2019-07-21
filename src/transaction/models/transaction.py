from django.db import models
from django.utils.translation import gettext as _

from wallet.models.wallet import Wallet

class Transaction(models.Model):
    MISSION_SUPPLEMENT = 'supplement'
    MISSION_CONCLUSION = 'conclusion'
    MISSION_DELEGATION = 'delegation'
    MISSION_DELEGATE_CHANGE = 'delegate_change'
    MISSION_DELEGATE_REMOVE = 'delegate_remove'
    MISSION_PAYMENT = 'payment'
    MISSION_APPROVED_PAYMENT = 'approved_payment'

    MISSIONS = (
        (MISSION_SUPPLEMENT, _("supplement")),
        (MISSION_CONCLUSION, _("conclusion")),
        (MISSION_DELEGATION, _("delegation")),
        (MISSION_DELEGATE_CHANGE, _("delegate change")),
        (MISSION_DELEGATE_REMOVE, _("delegate remove")),
        (MISSION_PAYMENT, _("payment")),
        (MISSION_APPROVED_PAYMENT, _("approved payment"))
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')

    tr_hash = models.CharField(_("hash"), max_length=100, db_index=True)
    address_from = models.CharField(_("address from"), max_length=100, null=True, db_index=True)
    address_to = models.CharField(_("address to"), max_length=100, null=True, db_index=True)
    mission = models.CharField(_("mission"), choices=MISSIONS, max_length=20, db_index=True)
    volume = models.FloatField(_("volume"), )
    commission = models.FloatField(_("commission"))
    committed = models.DateTimeField(_("committed"), db_index=True)
    comment = models.CharField(_("comment"), max_length=100, null=True, blank=True)


    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        ordering = ['-committed', ]
        constraints = [
            models.UniqueConstraint(
                fields=['wallet', 'tr_hash'],
                name="unique_transaction"
            )
        ]