import json
from datetime import datetime, timedelta, timezone

import requests
from omni_pro_oms import utils
from omni_pro_oms.models import Operation, OperationType, Task, Tenant, TenantOperation

base_url = "https://integration-core-oms-v3.omni.pro"


class ApiClient:
    def __init__(self, tenant: Tenant, timeout=30) -> None:
        self.tenant: Tenant = tenant
        self.timeout = timeout
        self.token = self.get_auth_token()
        self._set_api_models()

    def _set_api_models(self):
        from omni_pro_oms.core.catalog.product import ProductApi
        from omni_pro_oms.core.client.client import ClientApi
        from omni_pro_oms.core.rules.appointment import AppointmentApi
        from omni_pro_oms.core.rules.compute_method import ComputeMethodApi
        from omni_pro_oms.core.sale.order import OrderApi
        from omni_pro_oms.core.sale.order_line import OrderLineApi
        from omni_pro_oms.core.sale.sale import SaleApi
        from omni_pro_oms.core.sale.state import StateApi
        from omni_pro_oms.core.sale.tax import TaxApi
        from omni_pro_oms.core.stock.carrier_utils import CarrierSaveGuideApi
        from omni_pro_oms.core.stock.integration_stock import StockIntegrationApi
        from omni_pro_oms.core.stock.picking import PickingApi
        from omni_pro_oms.core.stock.warehouse import WarehouseApi
        from omni_pro_oms.core.utilities.file_record import FileRecordApi

        self.order = OrderApi(self)
        self.picking = PickingApi(self)
        self.compute_method = ComputeMethodApi(self)
        self.sale = SaleApi(self)
        self.stock_integration = StockIntegrationApi(self)
        self.client = ClientApi(self)
        self.warehouse = WarehouseApi(self)
        self.appointment = AppointmentApi(self)
        self.carrier_utils = CarrierSaveGuideApi(self)
        self.state = StateApi(self)
        self.file_record = FileRecordApi(self)
        self.product = ProductApi(self)
        self.order_line = OrderLineApi(self)
        self.tax = TaxApi(self)

    def call_api(
        self, method: str, endpoint: str, raise_status: bool = True, response_is_json: bool = True, **kwargs
    ) -> dict:
        if not kwargs.get("timeout", None):
            kwargs.update({"timeout": self.timeout})
        headers = {"Accept": "application/json", "Authorization": self.token}
        url = f"{self.tenant.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        if raise_status:
            response.raise_for_status()
        if response_is_json:
            return response.json()
        return response

    def get_auth_token(self):
        if (
            self.tenant.token_expires_at
            and (self.tenant.token_expires_at - datetime.now(timezone.utc)).total_seconds() > 600
        ):
            return self.tenant.token

        url = f"{self.tenant.base_url}/api/v1/auth/token"

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
        token = response.json().get("authentication_result", {}).get("token")
        expires_in = response.json().get("authentication_result", {}).get("expires_in")

        if expires_in:
            self.tenant.token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
            self.tenant.token = token
            self.tenant.save()

        return response.json().get("authentication_result", {}).get("token")
