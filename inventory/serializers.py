from rest_framework import serializers

from worklog.serializers import WorkLogSerializer
from vehicle.serializers import VehicleSerializer
from .models import Store, GRN


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "location",
            "current_coconuts",
            "current_bags",
            "is_active",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "current_coconuts", "current_bags", "created_at", "updated_at"]


class GRNSerializer(serializers.ModelSerializer):
    store_id = serializers.PrimaryKeyRelatedField(
        source="store", queryset=Store.objects.all(), write_only=True
    )
    store = StoreSerializer(read_only=True)
    
    # We allow linking a WorkLog and a Vehicle, but they are optional
    worklog_id = serializers.PrimaryKeyRelatedField(
        source="worklog", queryset=WorkLog.objects.all(), write_only=True, required=False, allow_null=True
    )
    vehicle_id = serializers.PrimaryKeyRelatedField(
        source="vehicle", queryset=Vehicle.objects.all(), write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = GRN
        fields = [
            "id",
            "store",
            "store_id",
            "worklog_id",
            "receipt_date",
            "coconut_count",
            "bag_count",
            "vehicle_id",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
