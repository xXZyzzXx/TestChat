from django.urls import include, path
from rest_framework.routers import DefaultRouter

from chat.views import MessageViewSet, ThreadViewSet

router = DefaultRouter()
router.register(r"thread", ThreadViewSet, basename="thread")
router.register(r"message", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
]
