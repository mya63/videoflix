from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authenticates users by reading the JWT access token from an HTTP-only cookie.
    """

    def authenticate(self, request):
        """
        Validates the access token from the cookie and returns the authenticated user.
        """

        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token