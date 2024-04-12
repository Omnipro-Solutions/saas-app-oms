from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from django.utils.translation import gettext_lazy as _
from omni_pro_base.models import OmniModel


def get_default_auth():
    """
    Generate value for default authentication field
    """
    return {
        "token": "123",
        "bearer_token": "Bearer your_token",
        "api_key": "qwerr",
        "auth2": {
            "client_id": "qweqr",
            "client_secret": "poiklo",
            "token_url": "https://auth-url.com",
            "grant_type": "client_credentials",
            "scope": "",
        },
        "auth1": {
            "consumer_key": "8w8rt9agjaf2iyc63jpeysoj9p5zd6li",
            "consumer_secret": "mh5riskd5pdf1uod95hrfx1807fejako",
            "access_token": "gjaf2iyc63jpeysoj9p5zd6li",
            "token_secret": "8w8rt9agjaf2iyc63jpeysoj9p5zd6li",
        },
        "custom": {
            "key": "value",
        },
    }


class Config(OmniModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    base_url = models.CharField(max_length=255, verbose_name=_("Base URL"))
    auth = models.JSONField(
        verbose_name=_("Auth"), blank=True, null=True, default=get_default_auth
    )
    token = models.JSONField(verbose_name=_("Token"), blank=True, null=True)

    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")


auditlog.register(Config)
