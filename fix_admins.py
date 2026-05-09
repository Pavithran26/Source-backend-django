import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bszone_backend.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from common.permissions import ROLE_ADMIN

def fix_superusers():
    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.role = ROLE_ADMIN
        profile.save()
        print(f"Fixed permissions for superuser: {user.username}")

if __name__ == "__main__":
    fix_superusers()
