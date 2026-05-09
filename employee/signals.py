from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Employee
from common.firebase_utils import sync_to_firestore, delete_from_firestore

@receiver(post_save, sender=Employee)
def sync_employee_to_firestore(sender, instance, created, **kwargs):
    data = {
        "id": str(instance.id),
        "employee_code": instance.employee_code,
        "full_name": instance.full_name,
        "role": instance.role,
        "department": instance.department,
        "designation": instance.designation,
        "phone_number": instance.phone_number,
        "daily_wage": str(instance.daily_wage),
        "is_active": instance.is_active,
        "updated_at": instance.updated_at.isoformat() if instance.updated_at else None
    }
    sync_to_firestore("employees", instance.id, data)

@receiver(post_delete, sender=Employee)
def delete_employee_from_firestore(sender, instance, **kwargs):
    delete_from_firestore("employees", instance.id)
