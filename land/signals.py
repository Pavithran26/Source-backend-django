from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Land
from common.firebase_utils import sync_to_firestore, delete_from_firestore

@receiver(post_save, sender=Land)
def sync_land_to_firestore(sender, instance, created, **kwargs):
    data = {
        "id": str(instance.id),
        "name": instance.name,
        "owner": instance.owner.name,
        "village": instance.village,
        "area_acres": str(instance.area_acres),
        "tree_count": instance.tree_count,
        "is_active": instance.is_active,
        "updated_at": instance.updated_at.isoformat() if instance.updated_at else None
    }
    sync_to_firestore("lands", instance.id, data)

@receiver(post_delete, sender=Land)
def delete_land_from_firestore(sender, instance, **kwargs):
    delete_from_firestore("lands", instance.id)
