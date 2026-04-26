from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from common.api import SafeAPIView, SafeGenericViewSet
from common.permissions import IsAdmin

from .serializers import UserSerializer, WorkspaceTokenObtainPairSerializer, ProfileUpdateSerializer
from .services import build_user_payload


class WorkspaceTokenObtainPairView(TokenObtainPairView):
    serializer_class = WorkspaceTokenObtainPairSerializer


class MeAPIView(SafeAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(build_user_payload(request.user))

    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(build_user_payload(request.user))


class UserViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    SafeGenericViewSet,
):
    queryset = User.objects.select_related("profile").order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    search_fields = ["username", "first_name", "last_name", "email", "profile__designation", "profile__role"]
    ordering_fields = ["username", "first_name", "email", "date_joined"]
