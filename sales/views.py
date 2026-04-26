from common.api import SafeModelViewSet
from common.permissions import IsAdminOrSupervisorOrReadOnly

from .models import Buyer, SalesEntry
from .serializers import BuyerSerializer, SalesEntrySerializer


class BuyerViewSet(SafeModelViewSet):
    queryset = Buyer.objects.all().order_by("name")
    serializer_class = BuyerSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = ["village"]
    search_fields = ["name", "phone_number", "village"]
    ordering_fields = ["name", "created_at"]


class SalesEntryViewSet(SafeModelViewSet):
    queryset = SalesEntry.objects.select_related("buyer", "land", "worklog").all().order_by("-sale_date", "-created_at")
    serializer_class = SalesEntrySerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = {
        "buyer": ["exact"],
        "land": ["exact"],
        "sale_date": ["exact", "gte", "lte"],
    }
    search_fields = ["buyer__name", "land__name", "notes"]
    ordering_fields = ["sale_date", "quantity", "unit_price", "created_at"]
