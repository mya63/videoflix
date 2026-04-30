from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        return Response(
            {
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
                "token": token,
                "uidb64": uidb64,
                "activation_link": f"/api/activate/{uidb64}/{token}/",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
        )

        return response


class LogoutView(generics.GenericAPIView):
    serializer_class = None
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = RefreshToken(refresh_token)
        token.blacklist()

        response = Response(
            {
                "detail": "Logout successful. All tokens will be deleted. Refresh token is now invalid."
            },
            status=status.HTTP_200_OK,
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class CookieTokenRefreshView(generics.GenericAPIView):
    serializer_class = None
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken(refresh_token)

        response = Response(
            {
                "detail": "Token refreshed",
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
        )

        return response
    
class ActivateView(generics.GenericAPIView):
    permission_classes = []
    serializer_class = None

    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"detail": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save()

        return Response(
            {"detail": "Account activated successfully."},
            status=status.HTTP_200_OK,
        )