from omni_pro_oms.permissions import TokenValidScope
from rest_framework import views


class OMNIAPIView(views.APIView):
    permission_classes = [TokenValidScope]
