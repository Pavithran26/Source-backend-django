from common.api import SafeModelViewSet
from common.permissions import IsAdminOrSupervisorOrReadOnly

from .models import Vehicle, VehicleUsageLog
from .serializers import VehicleSerializer, VehicleUsageLogSerializer


class VehicleViewSet(SafeModelViewSet):
    queryset = Vehicle.objects.all().order_by("registration_number")
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = {
        "vehicle_type": ["exact"],
        "is_active": ["exact"],
        "created_at": ["exact", "gte", "lte"],
    }
    search_fields = ["registration_number", "vehicle_type", "driver_name", "driver_phone"]
    ordering_fields = ["registration_number", "vehicle_type", "capacity", "created_at"]


class VehicleUsageLogViewSet(SafeModelViewSet):
    queryset = VehicleUsageLog.objects.select_related("vehicle").all().order_by("-usage_date", "-created_at")
    serializer_class = VehicleUsageLogSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = ["vehicle", "usage_date"]
    search_fields = ["vehicle__registration_number", "source", "destination", "notes"]
    ordering_fields = ["usage_date", "fuel_cost", "created_at"]
