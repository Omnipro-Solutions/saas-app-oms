from omni_pro_oms.models import Task
from omni_pro_oms import utils
from omni_pro_oms.core.api_client import ApiClient
from requests import Response
import json


class TaskApi(ApiClient):

    def __init__(self, task_id: int, timeout=30) -> None:
        self.task: Task = self._get_task(task_id)
        super().__init__(tenant=self.task.tenant_id, timeout=timeout)

    def _get_task(self, task_id: int):
        return Task.objects.get(id=task_id)

    def call_request(self, update_task: bool = False, **kwargs) -> Response:
        if not kwargs.get("timeout"):
            kwargs["timeout"] = self.timeout
        response: Response = utils.call_request(self.task.tenant_operation_id, **kwargs)
        if update_task:
            self.task_update_from_response(response)
        return response

    def task_update_from_response(self, response: Response):
        body_dest = json.loads(response.request.body.decode("utf-8"))
        response_dst = json.loads(response.content.decode("utf-8"))
        headers_dst = response.request.headers._store
        url_dst = response.request.url
        time_request = response.elapsed.total_seconds() * 1000

        self.task.url_dst = url_dst
        self.task.headers_dst = headers_dst
        self.task.body_dst = body_dest
        self.task.response_dst = response_dst
        self.task.time = time_request
        self.task.status = self.get_task_status_from_request_status_code(
            [response.status_code]
        )
        self.task.save()

    def get_task_status_from_request_status_code(self, status_codes):
        successful = all(status >= 200 and status < 300 for status in status_codes)
        unsuccessful = all(status >= 400 for status in status_codes)

        if successful and not unsuccessful:
            return "success"
        elif unsuccessful and not successful:
            return "error"
        else:
            return "partial_success"
