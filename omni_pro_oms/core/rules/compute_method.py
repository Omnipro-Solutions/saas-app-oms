endpoint_compute = "/api/v1/rules/compute-method"
from omni_pro_oms.core.api_client import ApiClient


class ComputeMethodApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def post_api(self, **kwargs):
        data = self.api_client.call_api(
            method="POST", endpoint=endpoint_compute, **kwargs
        )
        return data.get("result")
