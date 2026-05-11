from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from common.models import BaseModel
from worklog.models import WorkLog
from vehicle.models import Vehicle


class Store(BaseModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)
    current_coconuts = models.PositiveIntegerField(default=0)
    current_bags = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class GRN(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="grns")
    worklog = models.ForeignKey(WorkLog, on_delete=models.SET_NULL, null=True, blank=True, related_name="grns")
    receipt_date = models.DateField()
    coconut_count = models.PositiveIntegerField(default=0)
    bag_count = models.PositiveIntegerField(default=0)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="grns")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-receipt_date", "-created_at"]

    def __str__(self):
        return f"GRN - {self.store.name} on {self.receipt_date}"


@receiver(post_save, sender=GRN)
def update_store_inventory_on_save(sender, instance, created, **kwargs):
    store = instance.store
    # Note: In a full inventory system, we would also subtract Sales or Dispatches.
    # For now, we are aggregating the total received.
    all_grns = store.grns.all()
    store.current_coconuts = sum(grn.coconut_count for grn in all_grns)
    store.current_bags = sum(grn.bag_count for grn in all_grns)
    store.save(update_fields=["current_coconuts", "current_bags", "updated_at"])


@receiver(post_delete, sender=GRN)
def update_store_inventory_on_delete(sender, instance, **kwargs):
    store = instance.store
    all_grns = store.grns.all()
    store.current_coconuts = sum(grn.coconut_count for grn in all_grns)
    store.current_bags = sum(grn.bag_count for grn in all_grns)
    store.save(update_fields=["current_coconuts", "current_bags", "updated_at"])
