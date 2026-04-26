from django.contrib.auth.models import User


def build_user_payload(user: User) -> dict:
    profile = getattr(user, "profile", None)
    full_name = user.get_full_name().strip() or user.username
    return {
        "id": user.id,
        "username": user.username,
        "fullName": full_name,
        "email": user.email,
        "isActive": user.is_active,
        "role": getattr(profile, "role", "worker"),
        "phoneNumber": getattr(profile, "phone_number", ""),
        "designation": getattr(profile, "designation", ""),
        "preferredLanguage": getattr(profile, "preferred_language", "en"),
        "profileImage": profile.profile_image.url if profile and profile.profile_image else None,
    }
