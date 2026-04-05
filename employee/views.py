from common.api import SafeModelViewSet
from common.permissions import IsAdminOrSupervisorOrReadOnly

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(SafeModelViewSet):
    queryset = Employee.objects.all().order_by("full_name")
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = ["role", "department", "is_active"]
    search_fields = ["employee_code", "full_name", "department", "designation", "phone_number", "email"]
    ordering_fields = ["employee_code", "full_name", "joined_on", "daily_wage", "created_at"]
