from omni_pro_oms.core.api_client import ApiClient

endpoint_picking = "/api/v1/stock/picking"


class PickingApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, **kwargs):
        data = self.api_client.call_api(
            method="GET", endpoint=endpoint_picking, **kwargs
        )
        return data.get("pickings")
