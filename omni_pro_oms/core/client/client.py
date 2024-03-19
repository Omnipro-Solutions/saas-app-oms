from omni_pro_oms.core.api_client import ApiClient

endpoint_client = "/api/v1/client"


class ClientApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, **kwargs):
        data = self.api_client.call_api(method="GET", endpoint=endpoint_client, **kwargs)
        return data.get("clients")
