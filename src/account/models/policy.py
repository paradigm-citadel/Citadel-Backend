from django.db import models
from django.utils.translation import gettext as _


class PrivacyPolicy(models.Model):
    name = models.CharField(_("name"), max_length=30)
    file = models.FileField(_("file"), upload_to='privacy_policy')

    class Meta:
        verbose_name = _("privacy policy")
        verbose_name_plural = _("privacy policies")
