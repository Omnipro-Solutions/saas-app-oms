import json
import time

from django.core.exceptions import ObjectDoesNotExist
from omni_pro_oms import utils
from omni_pro_oms.core.api_client import ApiClient
from omni_pro_oms.models import Task
from requests import Response


class TaskApi(ApiClient):

    def __init__(self, task_id: int, celery_task_id: str = None, timeout=30) -> None:
        # self.task: Task = self._get_task(task_id)
        self.task: Task = TaskApi.get_task_with_retry(task_id)
        if celery_task_id:
            self._update_celery_task_id(celery_task_id)
            
        super().__init__(tenant=self.task.tenant_id, timeout=timeout)

    def _get_task(self, task_id: int):
        return Task.objects.get(id=task_id)

    @classmethod
    def get_task_with_retry(cls, task_id, max_retries=5, initial_delay=2):
        """Intenta obtener la tarea con reintentos y retraso progresivo."""
        for attempt in range(1, max_retries + 1):
            try:
                task = Task.objects.get(id=task_id)
                return task
            except Task.DoesNotExist:
                # calculo del retraso
                retry_delay = initial_delay + attempt
                if attempt < max_retries:
                    print(
                        f"Tarea {task_id} no encontrada. Reintentando en {retry_delay} segundos (intento {attempt}/{max_retries})..."
                    )
                    time.sleep(retry_delay)
                else:
                    print(f"Tarea {task_id} no encontrada después de {max_retries} intentos.")
                    raise ObjectDoesNotExist(f"Tarea {task_id} no encontrada después de {max_retries} intentos.")

    def call_request(self, update_task: bool = False, **kwargs) -> Response:
        if not kwargs.get("timeout"):
            kwargs["timeout"] = self.task.operation_id.timeout
        response: Response = utils.call_request(self.task.tenant_operation_id, **kwargs)
        if update_task:
            self.task_update_from_response(response)
        return response

    def task_update_from_response(self, response: Response, item: str = None):
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
        self.task.status = self.get_task_status_from_request_status_code([response.status_code])
        self.task.item = item
        self.task.save()

    def _update_celery_task_id(self, celery_task_id: str) -> None:
        """Actualiza el ID de la tarea de Celery en el modelo Task."""
        self.task.celery_task_id = celery_task_id
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
