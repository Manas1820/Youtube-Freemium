from django.urls import include, path
from rest_framework.routers import SimpleRouter

from backend.apps.accounts.views import ProfileViewSet
from backend.apps.ytcron.views.videos_view_set import VideosViewSet

router = SimpleRouter()
router.register("profile", ProfileViewSet, basename="profile")
router.register("freemium",VideosViewSet, basename="youtube")

versioned_urls = [path("", include(router.urls))]
