from rest_framework import viewsets
from django_filters import rest_framework as filters

from .models import Store, GRN
from .serializers import StoreSerializer, GRNSerializer


class StoreFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Store
        fields = ["name", "is_active"]


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by("name")
    serializer_class = StoreSerializer
    filterset_class = StoreFilter
    search_fields = ["name", "location", "notes"]


class GRNFilter(filters.FilterSet):
    receipt_date__gte = filters.DateFilter(field_name="receipt_date", lookup_expr="gte")
    receipt_date__lte = filters.DateFilter(field_name="receipt_date", lookup_expr="lte")
    store = filters.UUIDFilter(field_name="store__id")
    worklog = filters.UUIDFilter(field_name="worklog__id")

    class Meta:
        model = GRN
        fields = ["store", "worklog"]


class GRNViewSet(viewsets.ModelViewSet):
    queryset = GRN.objects.select_related("store", "worklog", "vehicle").all().order_by("-receipt_date", "-created_at")
    serializer_class = GRNSerializer
    filterset_class = GRNFilter
    search_fields = ["store__name", "notes"]
