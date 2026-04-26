from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from common.views import DashboardSummaryAPIView, EmployeeWorkReportAPIView, LandProductionReportAPIView, ProfitLossReportAPIView
from employee.views import EmployeeViewSet
from expenses.views import ExpenseViewSet
from land.views import LandOwnerViewSet, LandViewSet, LandLeasePaymentViewSet
from sales.views import BuyerViewSet, SalesEntryViewSet
from users.views import MeAPIView, UserViewSet, WorkspaceTokenObtainPairView
from vehicle.views import VehicleUsageLogViewSet, VehicleViewSet
from worklog.views import WorkLogViewSet

router = DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="user")
router.register("land-owners", LandOwnerViewSet, basename="land-owner")
router.register("lands", LandViewSet, basename="land")
router.register("land-payments", LandLeasePaymentViewSet, basename="land-payment")
router.register("employees", EmployeeViewSet, basename="employee")
router.register("vehicles", VehicleViewSet, basename="vehicle")
router.register("vehicle-usage", VehicleUsageLogViewSet, basename="vehicle-usage")
router.register("worklogs", WorkLogViewSet, basename="worklog")
router.register("buyers", BuyerViewSet, basename="buyer")
router.register("sales", SalesEntryViewSet, basename="sales-entry")
router.register("expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    path("auth/token", WorkspaceTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me", MeAPIView.as_view(), name="auth_me"),
    path("dashboard/summary", DashboardSummaryAPIView.as_view(), name="dashboard_summary"),
    path("reports/land-production", LandProductionReportAPIView.as_view(), name="report_land_production"),
    path("reports/employee-work", EmployeeWorkReportAPIView.as_view(), name="report_employee_work"),
    path("reports/profit-loss", ProfitLossReportAPIView.as_view(), name="report_profit_loss"),
    path("", include(router.urls)),
]
