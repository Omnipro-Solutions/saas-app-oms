from omni_pro_oms.core.api_client import ApiClient

endpoint_warehouse = "/api/v1/stock/warehouse"


class WarehouseApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, **kwargs):
        data = self.api_client.call_api(
            method="GET", endpoint=endpoint_warehouse, **kwargs
        )
        return data.get("warehouses")
