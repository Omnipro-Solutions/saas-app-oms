from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from omni_pro_base.models import OmniModel

STATUS_CHOICES = (
    ("waiting", "Waiting"),
    ("error", "Error"),
    ("success", "Success"),
    ("partial_success", "Partial Success"),
)


class Operation(OmniModel):

    class HttpMethod(models.TextChoices):
        GET = "GET", _("GET")
        POST = "POST", _("POST")
        PUT = "PUT", _("PUT")
        DELETE = "DELETE", _("DELETE")
        PATCH = "PATCH", _("PATCH")
        OPTIONS = "OPTIONS", _("OPTIONS")
        HEAD = "HEAD", _("HEAD")
        CONNECT = "CONNECT", _("CONNECT")
        TRACE = "TRACE", _("TRACE")

    class Score(models.TextChoices):
        LOW = "low", _("Low")
        MEDIUM = "medium", _("Medium")
        HIGH = "high", _("High")
        CRITICAL = "critical", _("Critical")

    class AuthType(models.TextChoices):
        TOKEN = ("token",)
        BEARER_TOKEN = ("bearer_token",)
        API_KEY = ("api_key",)
        AUTH2 = ("auth2",)
        AUTH1 = "auth1"
        CUSTOM = "custom"

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    destination = models.CharField(max_length=255, verbose_name=_("Destination"))
    score = models.CharField(
        choices=Score.choices, max_length=255, verbose_name=_("Score"), help_text=_("Level of priority")
    )
    endpoint_url = models.CharField(max_length=255, verbose_name=_("Endpoint URL"))
    http_method = models.CharField(choices=HttpMethod.choices, max_length=255, verbose_name=_("HTTP Method"), null=True)
    timeout = models.IntegerField(verbose_name=_("Timeout"), help_text=_("In seconds"))
    auth_type = models.CharField(choices=AuthType.choices, max_length=255, verbose_name=_("Auth Type"))
    headers = models.JSONField(verbose_name=_("Headers"), blank=True, null=True)
    success_clean_task_days = models.IntegerField(
        verbose_name=_("Success Clean Task Days"), help_text=_("In days"), null=True, blank=True
    )
    other_clean_task_days = models.IntegerField(
        verbose_name=_("Other Clean Task Days"), help_text=_("In days"), null=True, blank=True
    )
    packages_to_clean_count = models.IntegerField(
        verbose_name=_("Packages To Clean Count"), help_text=_("Number of packages to clean"), null=True, blank=True
    )
    active_notifications = models.BooleanField(verbose_name=_("Active Notifications"), default=False)
    emails = ArrayField(models.EmailField(), blank=True, default=list, verbose_name=_("Emails"))
    status_notifications = models.CharField(
        choices=STATUS_CHOICES,
        max_length=256,
        default="error",
        verbose_name=_("Status Notifications"),
    )

    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Operation")
        verbose_name_plural = _("Operations")


auditlog.register(Operation)
