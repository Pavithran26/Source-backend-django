from rest_framework import serializers

from employee.models import Employee
from employee.serializers import EmployeeSerializer
from land.models import Land
from land.serializers import LandSerializer
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer

from .models import WorkLog, WorkLogAssignment
from .services import sync_worklog_assignments


class WorkLogAssignmentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = WorkLogAssignment
        fields = ["id", "employee", "task_role", "units_completed", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class WorkLogSerializer(serializers.ModelSerializer):
    land_id = serializers.PrimaryKeyRelatedField(source="land", queryset=Land.objects.all(), write_only=True)
    supervisor_id = serializers.PrimaryKeyRelatedField(
        source="supervisor",
        queryset=Employee.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    vehicle_id = serializers.PrimaryKeyRelatedField(
        source="vehicle",
        queryset=Vehicle.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    worker_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        allow_empty=True,
    )
    land = LandSerializer(read_only=True)
    supervisor = EmployeeSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    assignments = WorkLogAssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = WorkLog
        fields = [
            "id",
            "work_date",
            "land",
            "land_id",
            "supervisor",
            "supervisor_id",
            "vehicle",
            "vehicle_id",
            "coconut_count",
            "bag_count",
            "latitude",
            "longitude",
            "photo_proof",
            "notes",
            "start_time",
            "end_time",
            "load_type",
            "transport_cost",
            "location",
            "worker_ids",
            "assignments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        worker_ids = validated_data.pop("worker_ids", [])
        worklog = super().create(validated_data)
        sync_worklog_assignments(worklog, worker_ids)
        return worklog

    def update(self, instance, validated_data):
        worker_ids = validated_data.pop("worker_ids", None)
        worklog = super().update(instance, validated_data)
        if worker_ids is not None:
            sync_worklog_assignments(worklog, worker_ids)
        return worklog
