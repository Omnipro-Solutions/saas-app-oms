from omni_pro_oms.models import Operation, OperationType, Tenant, TenantOperation, Task
from omni_pro_oms import utils
import json
import requests


base_url = "https://integration-core-oms-v3.omni.pro"


class ApiClient:
    def __init__(self, tenant: Tenant, timeout=30) -> None:
        self.tenant = tenant
        self.timeout = timeout
        self.token = self.get_auth_token()
        self._set_api_models()

    def _set_api_models(self):
        from omni_pro_oms.core.sale.order import OrderApi
        from omni_pro_oms.core.stock.picking import PickingApi
        from omni_pro_oms.core.rules.compute_method import ComputeMethodApi
        from omni_pro_oms.core.sale.sale import SaleApi
        from omni_pro_oms.core.stock.integration_stock import StockIntegrationApi

        self.order = OrderApi(self)
        self.picking = PickingApi(self)
        self.compute_method = ComputeMethodApi(self)
        self.sale = SaleApi(self)
        self.stock_integration = StockIntegrationApi(self)

    def call_api(self, method: str, endpoint: str, **kwargs) -> dict:
        kwargs.update({"timeout": self.timeout})
        headers = {"Accept": "application/json", "Authorization": self.token}
        url = f"{base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_auth_token(self):
        url = f"{base_url}/api/v1/auth/token"

        payload = json.dumps(
            {
                "client_secret": self.tenant.client_secret,
                "client_id": self.tenant.client_id,
                "tenant": self.tenant.code,
            }
        )
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        print("token status: ", response.status_code)
        return response.json().get("authentication_result", {}).get("token")
