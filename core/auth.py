import logging
from functools import wraps

from django.http import JsonResponse
from django.utils import timezone

from .models import AdminSession

logger = logging.getLogger(__name__)


def api_error(message: str, status: int) -> JsonResponse:
    return JsonResponse({"success": False, "message": message}, status=status)


def safe_api_endpoint(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ValueError as error:
            return api_error(str(error), 400)
        except Exception as error:
            logger.exception("Unhandled legacy API exception at %s", request.path, exc_info=error)
            return api_error("An unexpected error occurred. Please try again.", 500)

    return wrapped


def require_auth(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return api_error("Authentication required", 401)

        token = auth_header.replace("Bearer ", "", 1).strip()
        session = (
            AdminSession.objects.select_related("admin")
            .filter(token=token, expires_at__gt=timezone.now())
            .first()
        )

        if session is None:
            return api_error("Session expired or invalid", 401)

        request.admin_session = session
        return view_func(request, *args, **kwargs)

    return wrapped
