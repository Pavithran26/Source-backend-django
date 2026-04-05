from common.api import SafeModelViewSet
from common.permissions import IsAdminOrSupervisorOrReadOnly

from .models import Land, LandOwner
from .serializers import LandOwnerSerializer, LandSerializer


class LandOwnerViewSet(SafeModelViewSet):
    queryset = LandOwner.objects.all().order_by("name")
    serializer_class = LandOwnerSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = ["village"]
    search_fields = ["name", "phone_number", "village"]
    ordering_fields = ["name", "village", "created_at"]


class LandViewSet(SafeModelViewSet):
    queryset = Land.objects.select_related("owner").all().order_by("name")
    serializer_class = LandSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = ["owner", "village", "is_active"]
    search_fields = ["name", "village", "owner__name"]
    ordering_fields = ["name", "lease_start_date", "lease_end_date", "lease_amount", "tree_count", "created_at"]
