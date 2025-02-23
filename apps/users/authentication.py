from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        response = super().authenticate(request)
        if response is None:
            return None
        user, token = response
        if not user.is_approved:
            raise AuthenticationFailed('Your account is not approved yet.')
        return user, token
