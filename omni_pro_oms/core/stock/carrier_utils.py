from omni_pro_oms.core.api_client import ApiClient

endpoint_save_guide = "/api/v1/stock/carrier/save/guide"


class CarrierSaveGuideApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def save_guide(self, **kwargs):
        data = self.api_client.call_api(method="POST", endpoint=endpoint_save_guide, **kwargs)
        return data.get("response_standard")
