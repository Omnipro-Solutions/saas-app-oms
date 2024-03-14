from omni_pro_oms.core.api_client import ApiClient

endpoint_get_quants = "/api/v1/stock/search/quant/integration"
endpoint_set_quants = "/api/v1/stock/quant/integration"


class StockIntegrationApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_search_stock(self, **kwargs):
        response = self.api_client.call_api(
            method="POST", endpoint=endpoint_get_quants, **kwargs
        )
        data = {
            "message": response.get("response_standard", {}).get("message", "")
        }
        success = False

        if response.get("response_standard", {}).get("status_code") == 200:
            success = True
            data.update({
                "quants": response.get("quants", {}),
                "locations": response.get("locations", {}),
                "products": response.get("products", {})
            })

        return success, data

    def set_process_stock(self, **kwargs):
        data = self.api_client.call_api(
            method="POST", endpoint=endpoint_set_quants, **kwargs
        )
        success = False
        message = data.get("response_standard", {}).get("message", "")
        if data.get("response_standard", {}).get("status_code") == 200:
            success = True

        return success, message
