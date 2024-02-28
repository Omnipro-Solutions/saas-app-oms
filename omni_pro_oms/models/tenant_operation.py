import requests
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from omni_pro_base.models import OmniModel

from .config import Config
from .operation import Operation
from .operation_type import OperationType
from .tenant import Tenant


class TenantOperation(OmniModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"), null=True, blank=True)
    tenant_id = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, verbose_name=_("Tenant ID"), related_name="tenant_operations"
    )
    operation_id = models.ForeignKey(
        Operation, on_delete=models.CASCADE, verbose_name=_("Operation ID"), related_name="operation_tenant_operations"
    )
    operation_type_id = models.ForeignKey(
        OperationType,
        on_delete=models.CASCADE,
        verbose_name=_("Operation Type ID"),
        related_name="operation_type_tenant_operations",
    )
    config_id = models.ForeignKey(
        Config, on_delete=models.CASCADE, verbose_name=_("Config ID"), related_name="config_tenant_operations"
    )

    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.tenant_id.name} - {self.operation_type_id.name}"

    def get_oms_token(self):
        try:
            config = self.config_id

            if not config.token.get("token") or config.token.get("expired") <= timezone.now():
                token_response = requests.post(
                    config.base_url + config.auth.get("token_url"),
                    json={
                        "client_id": self.tenant_id.client_id,
                        "client_secret": self.tenant_id.client_secret,
                        "tenant": self.tenant_id.code,
                    },
                )
                if token_response.status_code != 200:
                    raise Exception(f"Token request failed with status code {token_response.status_code}")
                token_response_data = token_response.json()

                config.token["token"] = token_response_data["authentication_result"]["token"]
                config.token["expired"] == timezone.now() + timezone.timedelta(
                    seconds=token_response_data["authentication_result"]["expires_in"]
                )
                config.save()

            return config.token

        except Tenant.DoesNotExist:
            print(f"Tenant with code {self.code} does not exist.")
            raise Exception(f"Tenant with code {self.code} does not exist.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tenant_id", "operation_type_id"], name="unique_tenant_operation_type")
        ]
        verbose_name = _("Tenant Operation")
        verbose_name_plural = _("Tenant Operations")
        # ordering = ['created_at']


auditlog.register(TenantOperation)
