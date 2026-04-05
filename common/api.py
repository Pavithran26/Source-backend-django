from rest_framework import viewsets
from rest_framework.views import APIView


class SafeAPIView(APIView):
    """Base API view for endpoints that use the shared exception formatter."""


class SafeGenericViewSet(viewsets.GenericViewSet):
    """Base generic viewset for endpoints that use the shared exception formatter."""


class SafeModelViewSet(viewsets.ModelViewSet):
    """Base model viewset for endpoints that use the shared exception formatter."""
