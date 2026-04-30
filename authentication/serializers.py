from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "confirmed_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError(
                {"confirmed_password": "Passwords do not match."}
            )

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirmed_password")
        email = validated_data["email"]

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            is_active=False,
        )

        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["email"],
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid login credentials."}
            )

        attrs["user"] = user
        return attrs