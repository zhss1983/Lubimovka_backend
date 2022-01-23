from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.afisha.models import Event
from apps.afisha.pagination import AfishaPagination
from apps.afisha.schema.schema_extension import AFISHA_EVENTS_SCHEMA_DESCRIPTION
from apps.afisha.serializers import EventSerializer


@extend_schema(description=AFISHA_EVENTS_SCHEMA_DESCRIPTION)
class EventsAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Event.objects.filter(date_time__gte=timezone.now()).order_by("date_time")
    serializer_class = EventSerializer
    pagination_class = AfishaPagination


class GetCommonEventList(APIView):

    permission_classes = [
        IsAdminUser,
    ]

    def post(self, request, format=None):
        type = request.data["type"]
        common_event = {}
        if type:
            common_events = Event.objects.filter(type=type)
            common_event = {p.common_event.name: p.id for p in common_events}
        return Response(data=common_event, safe=False)
