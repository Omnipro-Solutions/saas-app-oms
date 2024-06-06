from datetime import datetime, timezone

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _
from omni_pro_base.models import OmniModel


class Tenant(OmniModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    code = models.CharField(max_length=255, verbose_name=_("Code"), unique=True)
    client_id = models.CharField(max_length=255, verbose_name=_("Client ID"))
    client_secret = models.CharField(max_length=255, verbose_name=_("Client Secret"))
    base_url = models.CharField(max_length=255, verbose_name=_("Base URL"))
    token = models.TextField(verbose_name=_("Token"), blank=True, null=True)
    token_expires_at = models.DateTimeField(verbose_name=_("Token Expires At"), blank=True, null=True)

    history = AuditlogHistoryField()

    @property
    def minutes_remaining(self):
        if self.token_expires_at:
            remaining_time = self.token_expires_at - datetime.now(timezone.utc)
            return remaining_time.total_seconds() // 60

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")


auditlog.register(Tenant)
