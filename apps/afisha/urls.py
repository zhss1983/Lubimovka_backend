from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.afisha.views import EventsAPIView, GetCommonEventList

router = DefaultRouter()
router.register(
    "events",
    EventsAPIView,
    basename="events",
)


afisha_urls = [
    path("afisha/", include(router.urls)),
    path(
        route="afisha/get-common-event-link/",
        view=GetCommonEventList.as_view(),
        name="common-event-models-links",
    ),
]

urlpatterns = [
    path("v1/", include(afisha_urls)),
]
