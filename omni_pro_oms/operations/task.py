from omni_pro_oms.models import Operation, OperationType, Task, Tenant, TenantOperation
from rest_framework.request import Request


class TaskOperation:

    @classmethod
    def create_task_from_request(cls, request: Request, tenant_operation: TenantOperation):
        tasks = []

        if isinstance(request, Request):
            if isinstance(request.data, list):
                data_list = request.data
            else:
                return cls._create_single_task(request, tenant_operation, request.data)
        elif isinstance(request, dict) and isinstance(request.get("data"), list):
            data_list = request.get("data")
        elif request is None:
            return cls._create_single_task(request, tenant_operation, None)

        for data_item in data_list:
            task = cls._create_single_task(request, tenant_operation, data_item)
            tasks.append(task)

        return tasks

    @staticmethod
    def _create_single_task(request: Request, tenant_operation: TenantOperation, data_item) -> Task:
        name = f"{tenant_operation.operation_type_id.name} {tenant_operation.tenant_id.name}"

        task = Task.objects.create(
            name=name,
            tenant_id=tenant_operation.tenant_id,
            operation_id=tenant_operation.operation_id,
            tenant_operation_id=tenant_operation,
            status="waiting",
            body_src=data_item,
            headers_src=dict(request.headers) if request else {},
            params_src=request.query_params if request else {},
            response_src={"success": True, "message": None},
            url_src=request.path if request and request.path else "",
            body_dst="",
            headers_dst="",
            params_dst="",
            response_dst="",
            url_dst="",
            time=0,
        )
        return task
