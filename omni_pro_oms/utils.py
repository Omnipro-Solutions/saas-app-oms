import json

import requests
from omni_pro_oms.models.task import Task
from omni_pro_oms.models.tenant import Tenant
from omni_pro_oms.models.tenant_operation import TenantOperation
from requests_oauthlib import OAuth1
from django.urls import resolve
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


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
        headers["Authorization"] = config.token

    return requests.request(**kwargs)


def retry_task_single(task):
    if task.status not in ["error", "waiting"]:
        return

    task_view = resolve(task.url_src)
    view = task_view.func.view_class()
    factory = APIRequestFactory()

    method = task.operation_id.http_method.lower()
    request_rest = getattr(factory, method)(task.url_src, task.body_src, content_type="application/json")

    request_rest = Request(request_rest, parsers=[view.parser_classes[0]])
    request_rest._full_data = task.body_src

    view_method = getattr(view, method)
    view_method(request=request_rest, **task_view.kwargs)