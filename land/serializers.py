from django.db.models import Sum
from rest_framework import serializers

from .models import Land, LandOwner, LandLeasePayment


class LandOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandOwner
        fields = ["id", "name", "phone_number", "village", "address", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class LandSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(source="owner", queryset=LandOwner.objects.all(), write_only=True)
    owner = LandOwnerSerializer(read_only=True)
    total_paid = serializers.SerializerMethodField()
    balance_due = serializers.SerializerMethodField()

    class Meta:
        model = Land
        fields = [
            "id",
            "owner",
            "owner_id",
            "name",
            "village",
            "area_acres",
            "lease_start_date",
            "lease_end_date",
            "lease_amount",
            "tree_count",
            "lease_notes",
            "is_active",
            "total_paid",
            "balance_due",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "total_paid", "balance_due"]

    def get_total_paid(self, obj):
        total = obj.payments.aggregate(total=Sum('amount'))['total']
        return total if total else 0

    def get_balance_due(self, obj):
        total_paid = self.get_total_paid(obj)
        return obj.lease_amount - total_paid

class LandLeasePaymentSerializer(serializers.ModelSerializer):
    land_id = serializers.PrimaryKeyRelatedField(source="land", queryset=Land.objects.all(), write_only=True)
    
    class Meta:
        model = LandLeasePayment
        fields = ["id", "land_id", "payment_date", "amount", "payment_type", "notes", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
