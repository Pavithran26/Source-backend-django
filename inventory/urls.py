from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, GRNViewSet

router = DefaultRouter()
router.register(r"stores", StoreViewSet, basename="store")
router.register(r"grns", GRNViewSet, basename="grn")

urlpatterns = [
    path("", include(router.urls)),
]
