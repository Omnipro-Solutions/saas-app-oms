
from omni_pro_oms.core.api_client import ApiClient

endpoint_order_line = "/api/v1/sales/order_line"


class OrderLineApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def put_api(self, **kwargs):
        data = self.api_client.call_api(method="PUT", endpoint=endpoint_order_line, **kwargs)
        return data.get("order_line")
