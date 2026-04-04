from django.db import models


class AdminCredential(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255)
    display_name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, default="admin")
    created_at = models.DateTimeField(auto_now_add=True)


class AdminSession(models.Model):
    admin = models.ForeignKey(AdminCredential, on_delete=models.CASCADE, related_name="sessions")
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


class Employee(models.Model):
    employee_code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    department = models.CharField(max_length=150)
    designation = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50)
    joined_on = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ("present", "Present"),
        ("late", "Late"),
        ("remote", "Remote"),
        ("absent", "Absent"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    attendance_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    worked_hours = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    check_in = models.CharField(max_length=10)
    check_out = models.CharField(max_length=10, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["employee", "attendance_date"], name="unique_employee_attendance_date")
        ]
