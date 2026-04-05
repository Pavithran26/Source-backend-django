from rest_framework import permissions, viewsets

from common.api import SafeModelViewSet
from common.permissions import IsAdminOrSupervisor, IsAuthenticatedWorkerOrAbove

from .models import WorkLog
from .serializers import WorkLogSerializer


class WorkLogViewSet(SafeModelViewSet):
    queryset = WorkLog.objects.select_related("land", "supervisor", "vehicle").prefetch_related(
        "assignments__employee"
    ).all().order_by("-work_date", "-created_at")
    serializer_class = WorkLogSerializer
    filterset_fields = ["land", "supervisor", "vehicle", "work_date"]
    search_fields = ["land__name", "land__village", "notes", "supervisor__full_name"]
    ordering_fields = ["work_date", "coconut_count", "bag_count", "created_at"]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsAuthenticatedWorkerOrAbove()]
        if self.request.method == "POST":
            return [IsAuthenticatedWorkerOrAbove()]
        return [IsAdminOrSupervisor()]
