from django.contrib.auth.models import User
from django.db import models

from common.models import BaseModel
from common.permissions import ROLE_ADMIN, ROLE_SUPERVISOR, ROLE_WORKER


class UserProfile(BaseModel):
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_SUPERVISOR, "Supervisor"),
        (ROLE_WORKER, "Worker"),
    ]

    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("ta", "Tamil"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_WORKER, db_index=True)
    phone_number = models.CharField(max_length=30, blank=True)
    designation = models.CharField(max_length=120, blank=True)
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default="en")
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self) -> str:
        return f"{self.user.username} ({self.role})"
