from omni_pro_oms.core.api_client import ApiClient

endpoint_attachment= "/api/v1/stock/attachment"


class AttachmentSaveGuideApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def post_api(self, **kwargs):
        response = self.api_client.call_api(
            method="POST", endpoint=endpoint_attachment, **kwargs
        )
        return response
