from omni_pro_oms.core.api_client import ApiClient

endpoint_product_integration = "/api/v1/catalog/product/integration"


class ProductIntegrationApi:

    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def product_integration(self, **kwargs):
        data = self.api_client.call_api(
            method="POST", endpoint=endpoint_product_integration, **kwargs
        )
        success = False
        message = data.get("response_standard", {}).get("message", "")
        if data.get("response_standard", {}).get("status_code") == 200:
            success = True

        return success, message
