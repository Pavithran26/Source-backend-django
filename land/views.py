from common.api import SafeModelViewSet
from common.permissions import IsAdminOrSupervisorOrReadOnly

from .models import Land, LandOwner, LandLeasePayment
from .serializers import LandOwnerSerializer, LandSerializer, LandLeasePaymentSerializer


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
    filterset_fields = {
        "owner": ["exact"],
        "village": ["exact"],
        "is_active": ["exact"],
        "lease_start_date": ["exact", "gte", "lte"],
    }
    search_fields = ["name", "village", "owner__name"]
    ordering_fields = ["name", "lease_start_date", "lease_end_date", "lease_amount", "tree_count", "created_at"]


class LandLeasePaymentViewSet(SafeModelViewSet):
    queryset = LandLeasePayment.objects.all().order_by("-payment_date", "-created_at")
    serializer_class = LandLeasePaymentSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = {
        "land": ["exact"],
        "payment_type": ["exact"],
        "payment_date": ["exact", "gte", "lte"],
    }
    search_fields = ["land__name", "notes"]
    ordering_fields = ["payment_date", "amount", "created_at"]
