from omni_pro_oms.core.api_client import ApiClient

endpoint_family = "/api/v1/catalog/family-attribute"


class FamilyApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_api(self, **kwargs):
        data = self.api_client.call_api(
            method="GET", endpoint=endpoint_family, **kwargs, raise_status=False, response_is_json=False
        )
        return data
