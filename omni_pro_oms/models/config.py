from datetime import timedelta
from logging import getLogger

import requests
from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from omni_pro_base.models import OmniModel

_logger = getLogger(__name__)


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
    auth = models.JSONField(verbose_name=_("Auth"), blank=True, null=True, default=get_default_auth)
    token = models.TextField(verbose_name=_("Token"), blank=True, null=True)
    expires_in = models.PositiveIntegerField(verbose_name=_("Time to token expiration"), blank=True, null=True)
    expires_at = models.DateTimeField(verbose_name=_("Date to token expiration"), blank=True, null=True)

    history = AuditlogHistoryField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    def is_token_auth2_valid(self):
        seconds_to_validate = 600
        if not self.token:
            _logger.error("Token is None or empty")
            return False

        if not self.expires_at:
            _logger.error("Token has no expiration date")
            return False

        is_expiring = (timezone.now() + timedelta(seconds=seconds_to_validate)) >= self.expires_at

        return not is_expiring

    def get_authenticate_auth2(self):
        try:
            if self.auth is None or self.auth.get("auth2") is None:
                _logger.error("No auth2 configuration found")
                return None

            credential_info = self.auth.get("auth2", {})

            grant_type = credential_info.get("grant_type", None)
            access_token_url = credential_info.get("token_url", None)
            client_id = credential_info.get("client_id", None)
            client_secret = credential_info.get("client_secret", None)
            scope = credential_info.get("scope", None)

            data = {
                "client_id": client_id,
                "client_secret": client_secret,
            }
            if grant_type == "client_credentials":
                data.update({"grant_type": grant_type})

            if scope:
                data.update({"scope": scope})

            request_params = {"method": "POST", "url": access_token_url, "data": data}
            response = requests.request(**request_params)

            body_response = response.json()

            return body_response

        except Exception as e:
            _logger.error(f"Error in call_api_authenticate: {e}")
            return None


auditlog.register(Config)
