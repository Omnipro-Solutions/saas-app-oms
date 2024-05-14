
from omni_pro_oms.core.api_client import ApiClient

endpoint_tax = "/api/v1/sales/tax"


class TaxApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, **kwargs):
        data = self.api_client.call_api(method="GET", endpoint=endpoint_tax, **kwargs)
        return data.get("tax")
