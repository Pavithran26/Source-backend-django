from common.api import SafeModelViewSet
from common.permissions import IsAdminOrSupervisorOrReadOnly

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(SafeModelViewSet):
    queryset = Expense.objects.select_related("land", "employee", "vehicle", "worklog").all().order_by(
        "-expense_date",
        "-created_at",
    )
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrSupervisorOrReadOnly]
    filterset_fields = {
        "expense_type": ["exact"],
        "land": ["exact"],
        "employee": ["exact"],
        "vehicle": ["exact"],
        "worklog": ["exact"],
        "expense_date": ["exact", "gte", "lte"],
    }
    search_fields = ["notes", "land__name", "employee__full_name", "vehicle__registration_number"]
    ordering_fields = ["expense_date", "amount", "created_at"]
