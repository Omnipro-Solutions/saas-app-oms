import json

import requests
from omni_pro_oms.models.task import Task
from omni_pro_oms.models.tenant import Tenant
from omni_pro_oms.models.tenant_operation import TenantOperation
from requests_oauthlib import OAuth1


def call_request(tenant_operation: TenantOperation, **kwargs):
    headers = tenant_operation.operation_id.headers or {}
    config = tenant_operation.config_id
    operation = tenant_operation.operation_id
    method = kwargs.get("method") if kwargs.get("method", None) else operation.http_method
    endpoint_url = kwargs.pop("endpoint_url") if kwargs.get("endpoint_url") else operation.endpoint_url

    url = config.base_url + endpoint_url

    kwargs.update(
        {
            "method": method,
            "url": url,
            "headers": headers,
        }
    )
    auth_type = operation.auth_type
    if auth_type == "auth1":
        config.auth.get(auth_type, {}).get("consumer_key")
        oauth = OAuth1(
            config.auth.get(auth_type, {}).get("consumer_key"),
            config.auth.get(auth_type, {}).get("consumer_secret"),
            config.auth.get(auth_type, {}).get("access_token"),
            config.auth.get(auth_type, {}).get("token_secret"),
        )
        kwargs["auth"] = oauth

    elif auth_type == "bearer_token":
        headers["Authorization"] = config.auth.get(auth_type)

    elif auth_type == "token":
        headers["Token"] = config.auth.get(auth_type)

    elif auth_type == "auth2":
        access_token = call_api_authenticate(credential_info=config.auth.get(auth_type, {}))
        headers["Authorization"] = f"Bearer {access_token}"

    return requests.request(**kwargs)


def call_api_authenticate(credential_info: dict = None):
    if credential_info is None:
        credential_info = {}
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
    access_token = body_response.get("access_token", None)

    return access_token
