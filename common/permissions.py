from rest_framework.permissions import BasePermission, SAFE_METHODS


ROLE_ADMIN = "admin"
ROLE_SUPERVISOR = "supervisor"
ROLE_WORKER = "worker"


def get_user_role(user) -> str:
    if getattr(user, "is_superuser", False):
        return ROLE_ADMIN
    profile = getattr(user, "profile", None)
    if profile and profile.role:
        return profile.role
    return ROLE_WORKER


def has_any_role(user, *roles: str) -> bool:
    return bool(user and user.is_authenticated and get_user_role(user) in roles)


class IsAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return has_any_role(request.user, ROLE_ADMIN)


class IsAdminOrSupervisor(BasePermission):
    def has_permission(self, request, view) -> bool:
        return has_any_role(request.user, ROLE_ADMIN, ROLE_SUPERVISOR)


class IsAdminOrSupervisorOrReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return has_any_role(request.user, ROLE_ADMIN, ROLE_SUPERVISOR)


class IsAuthenticatedWorkerOrAbove(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)
