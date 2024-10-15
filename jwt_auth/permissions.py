from rest_framework.permissions import BasePermission
from .authentication import JWTUser

class IsAuthenticatedWithJWT(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, JWTUser)