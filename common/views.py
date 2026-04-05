from datetime import date

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .api import SafeAPIView
from .services import build_dashboard_summary, get_employee_work_report, get_land_production_report, get_profit_loss_report


def _parse_date(value: str | None, field_name: str) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValidationError({field_name: "Use YYYY-MM-DD format."}) from error


class DashboardSummaryAPIView(SafeAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        target_date = _parse_date(request.query_params.get("date"), "date")
        return Response(build_dashboard_summary(target_date))


class LandProductionReportAPIView(SafeAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = _parse_date(request.query_params.get("date_from"), "date_from")
        date_to = _parse_date(request.query_params.get("date_to"), "date_to")
        return Response(get_land_production_report(date_from, date_to))


class EmployeeWorkReportAPIView(SafeAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = _parse_date(request.query_params.get("date_from"), "date_from")
        date_to = _parse_date(request.query_params.get("date_to"), "date_to")
        return Response(get_employee_work_report(date_from, date_to))


class ProfitLossReportAPIView(SafeAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = _parse_date(request.query_params.get("date_from"), "date_from")
        date_to = _parse_date(request.query_params.get("date_to"), "date_to")
        return Response(get_profit_loss_report(date_from, date_to))
