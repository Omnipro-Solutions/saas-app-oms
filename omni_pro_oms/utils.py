from requests_oauthlib import OAuth1
import requests
from omni_pro_oms.models.tenant_operation import TenantOperation
from omni_pro_oms.models.tenant import Tenant
from omni_sdk_oms.openapi_client.api.default_api import DefaultApi
from omni_sdk_oms.openapi_client.models.user_token import UserToken
from omni_sdk_oms.openapi_client.api_client import ApiClient
from omni_sdk_oms.openapi_client.configuration import Configuration
from urllib3 import HTTPResponse


def call_http_request(tenant_operation: TenantOperation, body=None, **kwargs):
    headers = tenant_operation.operation_id.headers
    config = tenant_operation.config_id
    url = kwargs.get("url")

    if not url:
        url = (
            tenant_operation.config_id.base_url
            + tenant_operation.operation_id.endpoint_url
        )

    request_params = {
        "method": tenant_operation.operation_id.http_method,
        "url": url,
        "headers": headers,
    }

    if config.auth == "auth1":
        oauth = OAuth1(
            config.auth[config.auth]["consumer_key"],
            config.auth[config.auth]["consumer_secret"],
            config.auth[config.auth]["access_token"],
            config.auth[config.auth]["token_secret"],
        )
        request_params["auth"] = oauth

    elif config.auth == "auth2":
        headers["Authorization"] = (
            config.auth[config.auth]["bearer_token"] + config.auth[config.auth]["token"]
        )

    if body:
        request_params["data"] = body

    response = requests.request(**request_params)

    return response


