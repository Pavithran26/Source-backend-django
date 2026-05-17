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
from inventory.views import StoreViewSet, GRNViewSet

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
router.register("stores", StoreViewSet, basename="store")
router.register("grns", GRNViewSet, basename="grn")

from django.http import JsonResponse
import traceback

def diag_view(request):
    diag_data = {}
    
    # 1. Database Connection check
    try:
        from django.db import connection
        connection.ensure_connection()
        diag_data["db_connection"] = "SUCCESSFUL"
        diag_data["db_vendor"] = connection.vendor
    except Exception as e:
        diag_data["db_connection"] = "FAILED"
        diag_data["db_error"] = str(e)
        diag_data["db_trace"] = traceback.format_exc()
        
    # 2. Firebase Env Variable check
    import os
    creds_env = os.getenv("FIREBASE_CREDENTIALS")
    diag_data["firebase_credentials_env_present"] = creds_env is not None
    if creds_env:
        diag_data["firebase_credentials_len"] = len(creds_env)
        try:
            import json
            parsed = json.loads(creds_env)
            diag_data["firebase_json_valid"] = True
            diag_data["firebase_project_id"] = parsed.get("project_id")
        except Exception as e:
            diag_data["firebase_json_valid"] = False
            diag_data["firebase_json_error"] = str(e)
            
    # 3. File existence check
    from pathlib import Path
    from django.conf import settings
    cert_path = Path(settings.BASE_DIR) / "serviceAccountKey.json"
    diag_data["service_account_file_present"] = cert_path.exists()
    
    # 4. Initialize Firebase App test
    try:
        from core.firebase_admin import get_firebase_app
        app = get_firebase_app()
        diag_data["firebase_app_init"] = "SUCCESSFUL"
        diag_data["firebase_app_name"] = app.name
    except Exception as e:
        diag_data["firebase_app_init"] = "FAILED"
        diag_data["firebase_error"] = str(e)
        diag_data["firebase_trace"] = traceback.format_exc()
        
    return JsonResponse(diag_data)

urlpatterns = [
    path("auth/diag", diag_view, name="diag_view"),
    path("auth/token", WorkspaceTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me", MeAPIView.as_view(), name="auth_me"),
    path("dashboard/summary", DashboardSummaryAPIView.as_view(), name="dashboard_summary"),
    path("reports/land-production", LandProductionReportAPIView.as_view(), name="report_land_production"),
    path("reports/employee-work", EmployeeWorkReportAPIView.as_view(), name="report_employee_work"),
    path("reports/profit-loss", ProfitLossReportAPIView.as_view(), name="report_profit_loss"),
    path("", include(router.urls)),
]
