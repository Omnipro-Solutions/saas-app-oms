from omni_pro_oms.core.api_client import ApiClient


class SaleApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, endpoint, **kwargs):
        data = self.api_client.call_api(method="GET", endpoint=endpoint, **kwargs)
        return data.get("sales")

    def post_api(self, endpoint, raise_status=True, response_is_json=True, **kwargs):
        response = self.api_client.call_api(
            method="POST", endpoint=endpoint, raise_status=raise_status, response_is_json=response_is_json, **kwargs
        )
        return response
