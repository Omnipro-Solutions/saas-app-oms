from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, Task
from omni_pro_oms import utils
import json
import requests
from omni_pro_oms.core.api_client import ApiClient


endpoint_order = "/api/v1/sales/order"


class OrderApi(ApiClient):
    def get_orders(self, **kwargs):
        data = self.call_api(method="GET", endpoint=endpoint_order, **kwargs)
        return data.get("orders")
