from omni_pro_oms.core.api_client import ApiClient

endpoint_Integration_operation = "/api/v1/stock/picking/integration-operation"


class IntegrationOperationApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def put_api(self, **kwargs):
        data = self.api_client.call_api(method="PUT", endpoint=endpoint_Integration_operation, **kwargs)
        return data.get("response_standard")
