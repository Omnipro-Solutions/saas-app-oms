from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, Task
from omni_pro_oms import utils
from omni_pro_oms.core.api_client import ApiClient
from requests_oauthlib import OAuth1
from requests import Response


class TaskApi(ApiClient):
    def __init__(self, task: Task, timeout=30) -> None:
        super().__init__(tenant=task.tenant_id, timeout=timeout)
        self.task: Task = task

    def call_request(self, **kwargs) -> Response:
        return utils.call_request(self.task.tenant_operation_id, **kwargs)
