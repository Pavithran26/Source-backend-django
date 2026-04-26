import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bszone_backend.settings")

django_application = get_wsgi_application()


def application(environ, start_response):
    if environ.get("PATH_INFO") == "/health":
        body = b'{"success":true,"message":"srk backend is healthy","data":{"uptime":0}}'
        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
        ]
        start_response("200 OK", headers)
        return [body]

    return django_application(environ, start_response)
