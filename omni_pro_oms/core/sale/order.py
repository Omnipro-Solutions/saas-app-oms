endpoint_order = "/api/v1/sales/order"
from omni_pro_oms.core.api_client import ApiClient


class OrderApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, **kwargs):
        data = self.api_client.call_api(method="GET", endpoint=endpoint_order, **kwargs)
        return data.get("orders")

    def put_api(self, **kwargs):
        data = self.api_client.call_api(method="PUT", endpoint=endpoint_order, **kwargs)
        return data.get("order")
