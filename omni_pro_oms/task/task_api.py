from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, Task
from omni_pro_oms import utils
from omni_pro_oms.core.api_client import ApiClient


class TaskApi(ApiClient):
    def __init__(self, task: Task, timeout=30) -> None:
        super().__init__(tenant=task.tenant_id, timeout=timeout)
        self.task = task
