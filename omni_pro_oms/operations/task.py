from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, Task
from rest_framework.request import Request
from urllib3 import HTTPResponse


class TaskOperation:

    @classmethod
    def create_task_from_request(
        cls, request: Request, tenant_operation: TenantOperation
    ) -> Task:
        name = f"{tenant_operation.operation_type_id.name} {tenant_operation.tenant_id.name}"
        task = Task.objects.create(
            name=name,
            tenant_id=tenant_operation.tenant_id,
            operation_id=tenant_operation.operation_id,
            tenant_operation_id=tenant_operation,
            status="waiting",
            body_src=request.data if request else "",
            headers_src=request.headers._store if request else "",
            params_src=request.query_params if request else "",
            response_src={"success": True, "message": None},
            url_src=request.stream.path if request else "",
            body_dst="",
            headers_dst="",
            params_dst="",
            response_dst="",
            url_dst="",
            time=0,
        )
        return task
