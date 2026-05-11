import os
import django

# Set up Django environment first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bszone_backend.settings')
django.setup()

# Now import Django models
from django.contrib.auth.models import User

def create_user():
    username = 'ranjithkumar'
    password = '123'
    
    print(f"Checking for user: {username}...")
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save() # This triggers the signal to create/update UserProfile
    
    if created:
        print(f"User '{username}' created successfully!")
    else:
        print(f"User '{username}' password updated successfully!")
    print("Account has full Admin privileges.")

if __name__ == "__main__":
    create_user()
