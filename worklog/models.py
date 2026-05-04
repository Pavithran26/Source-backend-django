from django.db import models

from common.models import BaseModel
from employee.models import Employee
from land.models import Land
from vehicle.models import Vehicle


class WorkLog(BaseModel):
    work_date = models.DateField(db_index=True)
    land = models.ForeignKey(Land, on_delete=models.PROTECT, related_name="worklogs")
    supervisor = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_worklogs",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="worklogs",
    )
    coconut_count = models.PositiveIntegerField(default=0)
    bag_count = models.PositiveIntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    photo_proof = models.ImageField(upload_to="worklog-proofs/", blank=True, null=True)
    notes = models.TextField(blank=True)
    
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    LOAD_CHOICES = (
        ('lease load', 'Lease Load'),
        ('Direct Load', 'Direct Load'),
    )
    load_type = models.CharField(max_length=20, choices=LOAD_CHOICES, null=True, blank=True)
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-work_date", "-created_at"]
        indexes = [
            models.Index(fields=["work_date", "land"]),
        ]

    def __str__(self) -> str:
        return f"{self.land.name} @ {self.work_date}"


class WorkLogAssignment(BaseModel):
    worklog = models.ForeignKey(WorkLog, on_delete=models.CASCADE, related_name="assignments")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="worklog_assignments")
    task_role = models.CharField(max_length=80, blank=True)
    units_completed = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["employee__full_name"]
        constraints = [
            models.UniqueConstraint(fields=["worklog", "employee"], name="unique_worklog_employee"),
        ]

    def __str__(self) -> str:
        return f"{self.employee.full_name} -> {self.worklog}"
