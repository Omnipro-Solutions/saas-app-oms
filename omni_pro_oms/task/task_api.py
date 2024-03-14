from omni_pro_oms.models import Task
from omni_pro_oms import utils
from omni_pro_oms.core.api_client import ApiClient
from requests import Response


class TaskApi(ApiClient):

    def __init__(self, task_id: int, timeout=30) -> None:
        self.task: Task = self._get_task(task_id)
        super().__init__(tenant=self.task.tenant_id, timeout=timeout)

    def _get_task(self, task_id: int):
        return Task.objects.get(id=task_id)

    def call_request(self, **kwargs) -> Response:
        return utils.call_request(self.task.tenant_operation_id, **kwargs)

    def get_task_status_from_request_status_code(self, status_codes):
        successful = all(status >= 200 and status < 300 for status in status_codes)
        unsuccessful = all(status >= 400 for status in status_codes)

        if successful and not unsuccessful:
            return "success"
        elif unsuccessful and not successful:
            return "error"
        else:
            return "partial_success"
