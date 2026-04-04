from django.apps import apps
from django.contrib.auth.hashers import check_password, make_password
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def seed_admin_credentials(sender, **kwargs):
    if sender.name != "core":
        return

    admin_model = apps.get_model("core", "AdminCredential")
    username = "Pavithran26"
    raw_password = "@Pavi4624"

    admin, created = admin_model.objects.get_or_create(
        username=username,
        defaults={
            "display_name": "Pavithran",
            "role": "admin",
            "password_hash": make_password(raw_password),
        },
    )

    if not created and not check_password(raw_password, admin.password_hash):
        admin.password_hash = make_password(raw_password)
        admin.save(update_fields=["password_hash"])
