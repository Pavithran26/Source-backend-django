from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.permissions import ROLE_WORKER

from .models import UserProfile
from .services import build_user_payload


class WorkspaceTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = getattr(user.profile, "role", ROLE_WORKER)
        token["name"] = user.get_full_name().strip() or user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = build_user_payload(self.user)
        return data


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, source="profile.role")
    phone_number = serializers.CharField(source="profile.phone_number", allow_blank=True, required=False)
    designation = serializers.CharField(source="profile.designation", allow_blank=True, required=False)
    preferred_language = serializers.ChoiceField(
        choices=UserProfile.LANGUAGE_CHOICES,
        source="profile.preferred_language",
        required=False,
    )
    password = serializers.CharField(write_only=True, required=False, allow_blank=False, min_length=8)
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    profile_image = serializers.ImageField(source="profile.profile_image", required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "password",
            "is_active",
            "role",
            "phone_number",
            "designation",
            "preferred_language",
            "profile_image",
        ]
        read_only_fields = ["id"]

    def to_representation(self, instance):
        return build_user_payload(instance)

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})
        password = validated_data.pop("password", None)
        full_name = validated_data.pop("full_name", "").strip()

        if full_name and not validated_data.get("first_name") and not validated_data.get("last_name"):
            parts = full_name.split(maxsplit=1)
            validated_data["first_name"] = parts[0]
            validated_data["last_name"] = parts[1] if len(parts) > 1 else ""

        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])

        profile = user.profile
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        password = validated_data.pop("password", None)
        full_name = validated_data.pop("full_name", "").strip()

        if full_name and not validated_data.get("first_name") and not validated_data.get("last_name"):
            parts = full_name.split(maxsplit=1)
            validated_data["first_name"] = parts[0]
            validated_data["last_name"] = parts[1] if len(parts) > 1 else ""

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if password:
            instance.set_password(password)

        instance.save()

        profile = instance.profile
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()

        return instance


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    profile_image = serializers.ImageField(source="profile.profile_image", required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["username", "password", "profile_image"]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        password = validated_data.pop("password", None)

        if "username" in validated_data:
            instance.username = validated_data["username"]

        if password:
            instance.set_password(password)

        instance.save()

        if profile_data:
            profile = instance.profile
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.save()

        return instance
