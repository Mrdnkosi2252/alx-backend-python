
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomJWTAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = super().authenticate(request)
        if auth:
            user, token = auth
            # Ensure user can only access their own data
            request.user = user
            return (user, token)
        raise AuthenticationFailed("Invalid token or user not authenticated")