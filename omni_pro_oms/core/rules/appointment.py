from omni_pro_oms.core.api_client import ApiClient


class AppointmentApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def post_api(self, endpoint,**kwargs):
        data = self.api_client.call_api(
            method="POST", endpoint=endpoint, **kwargs
        )
        return data.get("result")
