from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.permissions import ROLE_ADMIN

@receiver(post_save, sender=User)
def ensure_user_profile(sender, instance: User, created: bool, **kwargs):
    from .models import UserProfile
    role = ROLE_ADMIN if instance.is_superuser else "worker"
    if created:
        UserProfile.objects.create(user=instance, role=role)
    else:
        profile, created = UserProfile.objects.get_or_create(user=instance)
        if instance.is_superuser and profile.role != ROLE_ADMIN:
            profile.role = ROLE_ADMIN
            profile.save()
