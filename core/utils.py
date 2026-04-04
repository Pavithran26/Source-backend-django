from django.http import JsonResponse


def api_ok(message: str, data, status: int = 200) -> JsonResponse:
    return JsonResponse({"success": True, "message": message, "data": data}, status=status)
