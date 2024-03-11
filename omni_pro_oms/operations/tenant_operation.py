from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, task


class TenantOperationOperation:
    @classmethod
    def get_tenant_operation(
        cls, tenant_code: str, operation_type_code: str
    ) -> TenantOperation:
        tenant_operation = TenantOperation.objects.get(
            tenant_id__code=tenant_code, operation_type_id__code=operation_type_code
        )
        return tenant_operation
