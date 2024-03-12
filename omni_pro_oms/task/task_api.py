from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, Task
from rest_framework.request import Request
from omni_sdk_oms.openapi_client.api.default_api import DefaultApi
from omni_sdk_oms.openapi_client.models.user_token import UserToken
from omni_sdk_oms.openapi_client.api_client import ApiClient
from omni_sdk_oms.openapi_client.configuration import Configuration
from urllib3 import HTTPResponse
import requests


class TaskApi:
    def __init__(self, task: Task) -> None:
        self.task = task
        self.oms_api = DefaultApi()
        self.token = None
        self.tenant = self.task.tenant_id

    def _set_oms_api_token(self):
        user_token = UserToken(
            client_id=self.tenant.client_id,
            client_secret=self.tenant.client_secret,
            tenant=self.tenant.code,
        )
        res = self.oms_api.api_v1_auth_token_post(user_token)
        self.token = res.get("authentication_result", {}).get("token")

    def call_api_oms(self, endpoint: str, http_method: str, **kwargs) -> dict:
        if not self.token:
            self._set_oms_api_token()

        if self.token:
            headers = {"Accept": "application/json", "Authorization": self.token}
            url = f"{self.oms_api.api_client.configuration.host}{endpoint}"

            if http_method == "GET":
                print(kwargs)
                kwargs["headers"] = headers
                return requests.request(method=http_method, url=url, **kwargs).json()
            else:
                kwargs.update({"header_params": headers})
                return self.oms_api.api_client.call_api(
                    http_method, url, **kwargs
                ).response.json()

        else:
            raise Exception("Undefined token")
