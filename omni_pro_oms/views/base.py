from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import views


class OMNIAPIView(views.APIView):
    permission_classes = [TokenHasReadWriteScope]
    required_scopes = ["read", "write"]
