from django.contrib import admin

from apps.afisha.models import Event


class EventAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(EventAdmin, self).get_queryset(request)
        qs = qs.select_related(
            "common_event__masterclass",
            "common_event__reading",
            "common_event__performance",
        )
        return qs

    list_display = (
        "pk",
        "common_event",
        "type",
        "date_time",
        "paid",
        "pinned_on_main",
    )
    list_filter = ("type",)
    empty_value_display = "-пусто-"

    class Media:
        js = ("admin/afisha/js/ChoiceEvent.js",)


admin.site.register(Event, EventAdmin)
