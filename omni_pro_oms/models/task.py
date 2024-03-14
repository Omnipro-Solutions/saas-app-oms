from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _
from omni_pro_base.models import OmniModel

from .operation import Operation
from .tenant import Tenant
from .tenant_operation import TenantOperation

STATUS_CHOICES = (
    ("waiting", "Waiting"),
    ("error", "Error"),
    ("success", "Success"),
    ("partial_success", "Partial Success"),
)


class Task(OmniModel):
    name = models.CharField(max_length=256, verbose_name=_("Name"))
    tenant_id = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, verbose_name=_("Tenant"), related_name="tasks"
    )
    operation_id = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        verbose_name=_("Operation"),
        related_name="tasks",
    )
    tenant_operation_id = models.ForeignKey(
        TenantOperation,
        on_delete=models.CASCADE,
        verbose_name=_("TenantOperation"),
        related_name="tasks",
        null=True,
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=256,
        default="waiting",
        verbose_name=_("Status"),
    )
    body_src = models.JSONField(verbose_name=_("Body Source"), blank=True, null=True)
    headers_src = models.JSONField(
        verbose_name=_("Headers Source"), blank=True, null=True
    )
    params_src = models.JSONField(
        verbose_name=_("Params Source"), blank=True, null=True
    )
    response_src = models.JSONField(
        verbose_name=_("Response Source"), blank=True, null=True
    )
    url_src = models.CharField(
        max_length=256, verbose_name=_("URL Source"), blank=True, null=True
    )
    body_dst = models.JSONField(
        verbose_name=_("Body Destination"), blank=True, null=True
    )
    headers_dst = models.JSONField(
        verbose_name=_("Headers Destination"), blank=True, null=True
    )
    params_dst = models.JSONField(
        verbose_name=_("Params Destination"), blank=True, null=True
    )
    response_dst = models.JSONField(
        verbose_name=_("Response Destination"), blank=True, null=True
    )
    url_dst = models.CharField(
        max_length=256, verbose_name=_("URL Destination"), blank=True, null=True
    )
    time = models.IntegerField(
        verbose_name=_("Time"), help_text=_("In milliseconds"), blank=True, null=True
    )

    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


auditlog.register(Task)
