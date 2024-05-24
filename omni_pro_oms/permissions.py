import requests
from django.conf import settings
from rest_framework import permissions


class TokenValidScope(permissions.BasePermission):
    message = "Invalid or expired token."

    def has_permission(self, request, view):
        auth = request.headers.get("Authorization", None)
        if auth:
            token = auth.split(" ")[-1]
            url = settings.AUTH_BASE_URL + f"/auth/token/validate/?token={token}"
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(url, headers=headers)
            return response.status_code == 200

        token = request.headers.get("token", None)
        if token:
            url = settings.AUTH_BASE_URL + "/auth/user/validate/"
            headers = {"Authorization": f"Token {token}"}
            response = requests.get(url, headers=headers)
            return response.status_code == 200

        return False
