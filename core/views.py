import json
import secrets
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_safe

from .auth import api_error, require_auth, safe_api_endpoint
from .models import AdminCredential, AdminSession, AttendanceRecord, Employee
from .utils import api_ok


def _parse_json(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON body")


def _serialize_employee(employee: Employee):
    joined_on = employee.joined_on
    if isinstance(joined_on, str):
        joined_on = date.fromisoformat(joined_on)

    return {
        "id": str(employee.id),
        "employeeCode": employee.employee_code,
        "fullName": employee.full_name,
        "department": employee.department,
        "designation": employee.designation,
        "email": employee.email,
        "phoneNumber": employee.phone_number,
        "joinedOn": joined_on.isoformat(),
    }


def _serialize_attendance(record: AttendanceRecord):
    employee = record.employee
    attendance_date = record.attendance_date
    if isinstance(attendance_date, str):
        attendance_date = date.fromisoformat(attendance_date)

    return {
        "id": str(record.id),
        "employeeId": str(employee.id),
        "employeeCode": employee.employee_code,
        "employeeName": employee.full_name,
        "department": employee.department,
        "designation": employee.designation,
        "date": attendance_date.isoformat(),
        "status": record.status,
        "workedHours": float(record.worked_hours),
        "checkIn": record.check_in,
        "checkOut": record.check_out,
        "notes": record.notes,
    }


def _parse_iso_date(value: str, field_name: str):
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        raise ValueError(f"{field_name} must be a valid date in YYYY-MM-DD format")


def _validate_employee_payload(payload):
    required_fields = [
        "employeeCode",
        "fullName",
        "department",
        "designation",
        "email",
        "phoneNumber",
        "joinedOn",
    ]

    for field in required_fields:
        if not str(payload.get(field, "")).strip():
            raise ValueError(f"{field} is required")

    try:
        validate_email(payload["email"])
    except ValidationError as error:
        raise ValueError("A valid email is required") from error

    return {
        "employee_code": str(payload["employeeCode"]).strip(),
        "full_name": str(payload["fullName"]).strip(),
        "department": str(payload["department"]).strip(),
        "designation": str(payload["designation"]).strip(),
        "email": str(payload["email"]).strip(),
        "phone_number": str(payload["phoneNumber"]).strip(),
        "joined_on": _parse_iso_date(payload["joinedOn"], "joinedOn"),
    }


@safe_api_endpoint
@require_safe
def health(request):
    return api_ok(
        "BSZone backend is healthy",
        {
            "uptime": 0,
        },
    )


@safe_api_endpoint
@require_GET
def api_index(request):
    return api_ok("BSZone API ready", {"modules": ["auth", "employees", "attendance"]})


@safe_api_endpoint
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        payload = _parse_json(request)
    except ValueError as error:
        return api_error(str(error), 400)

    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", "")).strip()

    if not username or not password:
        return api_error("Username and password are required", 400)

    admin = AdminCredential.objects.filter(username=username).first()
    if admin is None or not check_password(password, admin.password_hash):
        return api_error("Invalid username or password", 401)

    expires_at = timezone.now() + timedelta(hours=12)
    token = secrets.token_hex(48)
    AdminSession.objects.create(admin=admin, token=token, expires_at=expires_at)

    return api_ok(
        "Login successful",
        {
            "token": token,
            "user": {
                "id": str(admin.id),
                "name": admin.display_name,
                "username": admin.username,
                "role": admin.role,
            },
            "expiresAt": expires_at.isoformat(),
        },
    )


@safe_api_endpoint
@require_GET
@require_auth
def me(request):
    admin = request.admin_session.admin
    return api_ok(
        "Session is valid",
        {
            "user": {
                "id": str(admin.id),
                "name": admin.display_name,
                "username": admin.username,
                "role": admin.role,
            }
        },
    )


@safe_api_endpoint
@require_http_methods(["GET", "POST"])
@csrf_exempt
@require_auth
def employees(request):
    if request.method == "GET":
        items = Employee.objects.order_by("-created_at")
        return api_ok("Employees fetched", [_serialize_employee(item) for item in items])

    try:
        payload = _parse_json(request)
        employee_data = _validate_employee_payload(payload)
    except ValueError as error:
        return api_error(str(error), 400)

    try:
        employee = Employee.objects.create(**employee_data)
    except IntegrityError:
        return api_error("Employee code or email already exists", 409)

    return api_ok("Employee created successfully", _serialize_employee(employee), status=201)


@safe_api_endpoint
@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
@require_auth
def employee_detail(request, employee_id: int):
    employee = Employee.objects.filter(id=employee_id).first()
    if employee is None:
        return api_error("Employee was not found", 404)

    if request.method == "GET":
        return api_ok("Employee fetched", _serialize_employee(employee))

    if request.method == "DELETE":
        employee.delete()
        return api_ok("Employee deleted successfully", {"id": str(employee_id)})

    try:
        payload = _parse_json(request)
        employee_data = _validate_employee_payload(payload)
    except ValueError as error:
        return api_error(str(error), 400)

    for field, value in employee_data.items():
        setattr(employee, field, value)

    try:
        employee.save()
    except IntegrityError:
        return api_error("Employee code or email already exists", 409)

    return api_ok("Employee updated successfully", _serialize_employee(employee))


@safe_api_endpoint
@require_GET
@require_auth
def attendance_summary(request):
    today = timezone.now().date()
    records = list(
        AttendanceRecord.objects.filter(attendance_date=today).select_related("employee")
    )
    present_count = len([record for record in records if record.status in {"present", "late", "remote"}])
    late_count = len([record for record in records if record.status == "late"])
    remote_count = len([record for record in records if record.status == "remote"])
    rate = round((present_count / len(records)) * 100) if records else 0

    return api_ok(
        "Attendance summary fetched",
        {
            "todayPresent": present_count,
            "lateArrivals": late_count,
            "remoteEmployees": remote_count,
            "attendanceRate": rate,
        },
    )


@safe_api_endpoint
@require_GET
@require_auth
def attendance_records(request):
    records = AttendanceRecord.objects.select_related("employee").order_by("-attendance_date", "employee__full_name")
    return api_ok("Attendance records fetched", [_serialize_attendance(record) for record in records])


@safe_api_endpoint
@csrf_exempt
@require_http_methods(["POST"])
@require_auth
def mark_attendance(request):
    try:
        payload = _parse_json(request)
    except ValueError as error:
        return api_error(str(error), 400)

    employee_id = payload.get("employeeId")
    if not employee_id:
        return api_error("employeeId is required", 400)

    employee = Employee.objects.filter(id=employee_id).first()
    if employee is None:
        return api_error("Selected employee was not found", 404)

    try:
        attendance_date = _parse_iso_date(payload.get("date", ""), "date")
    except ValueError as error:
        return api_error(str(error), 400)

    try:
        record = AttendanceRecord.objects.create(
            employee=employee,
            attendance_date=attendance_date,
            status=str(payload.get("status", "")).strip(),
            worked_hours=Decimal(str(payload.get("workedHours", "0"))),
            check_in=str(payload.get("checkIn", "")).strip(),
            check_out=str(payload.get("checkOut", "")).strip() or None,
            notes=str(payload.get("notes", "")).strip() or None,
        )
    except IntegrityError:
        return api_error("Attendance already exists for this employee on the selected date", 409)
    except Exception as error:
        return api_error(str(error), 400)

    return api_ok("Attendance marked successfully", _serialize_attendance(record), status=201)
