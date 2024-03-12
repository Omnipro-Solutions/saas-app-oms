from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, Task
from rest_framework.request import Request
from omni_sdk_oms.openapi_client.api.default_api import DefaultApi
from omni_sdk_oms.openapi_client.models.user_token import UserToken
from omni_sdk_oms.openapi_client.api_client import ApiClient
from omni_sdk_oms.openapi_client.configuration import Configuration
from urllib3 import HTTPResponse
from omni_pro_oms import utils
import requests
import urllib3


class TaskApi:

    def __init__(self, task: Task, timeout=30) -> None:
        self.task = task
        self.oms_api = DefaultApi()
        self.token = None
        self.tenant = self.task.tenant_id
        self.timeout = timeout

    def _set_oms_api_token(self):
        self.token = utils.get_oms_auth_token(self.tenant)

    def call_oms_api(self, method: str, endpoint, **kwargs) -> dict:
        if not self.token:
            self._set_oms_api_token()
        kwargs.update({"timeout": self.timeout})
        return utils.call_oms_api(
            method=method, endpoint=endpoint, token=self.token, **kwargs
        )
