from django.contrib import admin

from .models import AdminCredential, AdminSession, AttendanceRecord, Employee

admin.site.register(AdminCredential)
admin.site.register(AdminSession)
admin.site.register(Employee)
admin.site.register(AttendanceRecord)
