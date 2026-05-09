from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import WorkLog
from common.firebase_utils import sync_to_firestore, delete_from_firestore

@receiver(post_save, sender=WorkLog)
def sync_worklog_to_firestore(sender, instance, created, **kwargs):
    data = {
        "id": str(instance.id),
        "work_date": instance.work_date.isoformat(),
        "land": instance.land.name,
        "supervisor": instance.supervisor.full_name if instance.supervisor else "None",
        "coconut_count": instance.coconut_count,
        "bag_count": instance.bag_count,
        "load_type": instance.load_type,
        "location": instance.location,
        "updated_at": instance.updated_at.isoformat() if instance.updated_at else None
    }
    sync_to_firestore("worklogs", instance.id, data)

@receiver(post_delete, sender=WorkLog)
def delete_worklog_from_firestore(sender, instance, **kwargs):
    delete_from_firestore("worklogs", instance.id)
