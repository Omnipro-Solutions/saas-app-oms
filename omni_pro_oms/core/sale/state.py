from omni_pro_oms.core.api_client import ApiClient
endpoint_state = "/api/v1/sales/state"

class StateApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, **kwargs):
        data = self.api_client.call_api(method="GET", endpoint=endpoint_state, **kwargs)
        return data.get("states")
