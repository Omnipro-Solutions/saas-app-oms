from omni_pro_oms.permissions import TokenValidScope
from rest_framework import permissions, views


class OMNIAPIView(views.APIView):
    permission_classes = [TokenValidScope]


class InternalBaseView(views.APIView):
    permission_classes = [permissions.AllowAny]
