from django.contrib import admin

from apps.articles.models import NewsItem, NewsItemContent
from apps.content_pages.admin import BaseContentInline, BaseContentPageAdmin
from apps.core.mixins import InlineReadOnlyMixin, PreviewButtonMixin, StatusButtonMixin


class NewsItemContentInline(InlineReadOnlyMixin, BaseContentInline):
    model = NewsItemContent


@admin.register(NewsItem)
class NewsItemAdmin(StatusButtonMixin, PreviewButtonMixin, BaseContentPageAdmin):
    list_display = (
        "title",
        "description",
        "pub_date",
        "image_preview_list_page",
        "status",
        "creator_name",
    )
    readonly_fields = (
        "status",
        "image_preview_change_page",
        "creator_name",
    )
    inlines = (NewsItemContentInline,)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
                    "title",
                    "pub_date",
                    "description",
                    ("image_preview_change_page", "image"),
                    "creator_name",
                )
            },
        ),
    )
    other_readonly_fields = (
        "status",
        "title",
        "pub_date",
        "description",
        "image_preview_change_page",
        "image",
        "creator_name",
    )
