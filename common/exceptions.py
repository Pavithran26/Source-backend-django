import logging

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def _to_plain_data(value):
    if isinstance(value, ErrorDetail):
        return str(value)
    if isinstance(value, list):
        return [_to_plain_data(item) for item in value]
    if isinstance(value, tuple):
        return [_to_plain_data(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_plain_data(item) for key, item in value.items()}
    return value


def _extract_message(data, status_code: int) -> str:
    if isinstance(data, dict):
        detail = data.get("detail")
        if isinstance(detail, str) and detail:
            return detail

        non_field_errors = data.get("non_field_errors")
        if isinstance(non_field_errors, list) and non_field_errors:
            first_error = non_field_errors[0]
            if isinstance(first_error, str) and first_error:
                return first_error

        for value in data.values():
            if isinstance(value, list) and value:
                first_error = value[0]
                if isinstance(first_error, str) and first_error:
                    return first_error
            if isinstance(value, str) and value:
                return value

    if status_code == status.HTTP_400_BAD_REQUEST:
        return "Validation failed"
    if status_code == status.HTTP_401_UNAUTHORIZED:
        return "Authentication failed"
    if status_code == status.HTTP_403_FORBIDDEN:
        return "Permission denied"
    if status_code == status.HTTP_404_NOT_FOUND:
        return "Resource not found"

    return "Request failed"


def workspace_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get("request")

    if response is None:
        logger.exception(
            "Unhandled API exception at %s",
            getattr(request, "path", "unknown"),
            exc_info=exc,
        )
        return Response(
            {
                "success": False,
                "message": "An unexpected error occurred. Please try again.",
                "errors": {},
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    normalized_errors = _to_plain_data(response.data)
    response.data = {
        "success": False,
        "message": _extract_message(normalized_errors, response.status_code),
        "errors": normalized_errors,
    }
    return response
