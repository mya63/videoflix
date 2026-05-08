
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .tasks import send_activation_email

from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Creates a new inactive user account and returns an activation link.
    """

    serializer_class = RegisterSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        """
        Validates registration data, creates the user and generates activation data.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = request.build_absolute_uri(
            f"/api/activate/{uidb64}/{token}/"
    )
        
        send_activation_email(user.email, activation_link)

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
    """
    Authenticates a user and stores JWT tokens in HTTP-only cookies.
    """

    serializer_class = LoginSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """
        Validates login data and sets access and refresh token cookies.
        """

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
            secure=True,
            samesite="None",
            
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None",
            
        )

        return response


class LogoutView(generics.GenericAPIView):
    """
    Logs out the user by blacklisting the refresh token and deleting cookies.
    """

    serializer_class = None
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """
        Invalidates the refresh token and removes authentication cookies.
        """

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

        response.delete_cookie("access_token", samesite="None")
        response.delete_cookie("refresh_token", samesite="None")

        return response


class CookieTokenRefreshView(generics.GenericAPIView):
    """
    Refreshes the access token by reading the refresh token from cookies.
    """

    serializer_class = None
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """
        Creates a new access token and stores it as an HTTP-only cookie.
        """

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
            secure=True,
            samesite="None",
        )

        return response


class ActivateView(generics.GenericAPIView):
    """
    Activates an inactive user account using uid and token from the activation link.
    """

    permission_classes = []
    serializer_class = None
    authentication_classes = []

    def get(self, request, uidb64, token):
        """
        Validates the activation token and activates the matching user account.
        """

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

        return redirect("https://mya63.github.io/project.Videoflix/")
    
class PasswordResetView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = None

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"email": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"email": "No user with this email exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = request.build_absolute_uri(
            f"/api/password_confirm/{uidb64}/{token}/"
        )

        html_content = render_to_string(
            "emails/password_reset_email.html",
            {"reset_link": reset_link},
        )

        email_message = EmailMultiAlternatives(
            subject="Reset your Videoflix password",
            body=f"Click here to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return Response(
            {"detail": "An email has been sent to reset your password."},
            status=status.HTTP_200_OK,
        )


class PasswordConfirmView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = None

    def get(self, request, uidb64, token):
        return redirect(
            f"https://mya63.github.io/project.Videoflix/pages/auth/confirm_password.html?uid={uidb64}&token={token}"
        )

    def post(self, request, uidb64, token):
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if new_password != confirm_password:
            return Response(
                {"confirm_password": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"detail": "Invalid password reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid password reset link."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validate_password(new_password, user)
        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Your Password has been successfully reset."},
            status=status.HTTP_200_OK,
        )
        