from django.urls import path

from . import views

urlpatterns = [
    path("health", views.health),
    path("api/", views.api_index),
    path("api/auth/login", views.login),
    path("api/auth/me", views.me),
    path("api/employees", views.employees),
    path("api/attendance/summary", views.attendance_summary),
    path("api/attendance/records", views.attendance_records),
    path("api/attendance/mark", views.mark_attendance),
]
