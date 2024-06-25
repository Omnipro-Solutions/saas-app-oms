endpoint_order = "/api/v1/sales/order"
from omni_pro_oms.core.api_client import ApiClient


class OrderApi:
    def __init__(self, api_client: ApiClient, raw_response=False):
        self.api_client = api_client
        self.raw_response = raw_response

    def get_api(self, **kwargs):
        try:
            data = self.api_client.call_api(method="GET", endpoint=endpoint_order, **kwargs)
            if self.raw_response:
                return data
            return data.get("orders")
        except Exception as e:
            raise {"error": str(e)}

    def put_api(self, **kwargs):
        try:
            data = self.api_client.call_api(method="PUT", endpoint=endpoint_order, **kwargs)
            if self.raw_response:
                return data
            return data.get("order")
        except Exception as e:
            raise {"error": str(e)}
