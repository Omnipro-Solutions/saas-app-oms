from omni_pro_oms.core.api_client import ApiClient

endpoint_file_record = "/api/v1/utilities/file_record"

class FileRecordApi:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def post_api(self, **kwargs):
        response = self.api_client.call_api(
            method="POST", endpoint=endpoint_file_record, **kwargs
        )
        return response
