from typing import Any, Optional

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q


class Command(BaseCommand):
    help = "Устанавливает права для групп пользователей Администратор и Редактор"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            editors_permissions = Permission.objects.filter(
                Q(codename__endswith="_achievement")
                | Q(codename__endswith="_author")
                | Q(codename__endswith="_banner")
                | Q(codename__endswith="_blogitem")
                | Q(codename__endswith="_blogitemcontent")
                | Q(codename__endswith="_blogperson")
                | Q(codename__endswith="_commonevent")
                | Q(codename__endswith="_contentpersonrole")
                | Q(codename__endswith="_contenttype")
                | Q(codename__endswith="_event")
                | Q(codename__endswith="_extendedperson")
                | Q(codename__endswith="_festival")
                | Q(codename__endswith="_festivalteam")
                | Q(codename__endswith="_image")
                | Q(codename__endswith="_imagesblock")
                | Q(codename__endswith="_link")
                | Q(codename__endswith="_masterclass")
                | Q(codename__endswith="_newsitem")
                | Q(codename__endswith="_newsitemcontent")
                | Q(codename__endswith="_orderedimage")
                | Q(codename__endswith="_orderedperformance")
                | Q(codename__endswith="_orderedplay")
                | Q(codename__endswith="_orderedvideo")
                | Q(codename__endswith="_otherlink")
                | Q(codename__endswith="_otherplay")
                | Q(codename__endswith="_participationapplicationfestival")
                | Q(codename__endswith="_partner")
                | Q(codename__endswith="_performance")
                | Q(codename__endswith="_performancemediareview")
                | Q(codename__endswith="_performancereview")
                | Q(codename__endswith="_performancesblock")
                | Q(codename__endswith="_person")
                | Q(codename__endswith="_personsblock")
                | Q(codename__endswith="_play")
                | Q(codename__endswith="_place")
                | Q(codename__endswith="_playsblock")
                | Q(codename__endswith="_preamble")
                | Q(codename__endswith="_pressrelease")
                | Q(codename__endswith="_programtype")
                | Q(codename__endswith="_project")
                | Q(codename__endswith="_projectcontent")
                | Q(codename__endswith="_question")
                | Q(codename__endswith="_quote")
                | Q(codename__endswith="_reading")
                | Q(codename__endswith="_role")
                | Q(codename__endswith="_roletype")
                | Q(codename__endswith="_setting")
                | Q(codename__endswith="_settingafishascreen")
                | Q(codename__endswith="_settingemail")
                | Q(codename__endswith="_settingfirstscreen")
                | Q(codename__endswith="_settinggeneral")
                | Q(codename__endswith="_settingmain")
                | Q(codename__endswith="_site")
                | Q(codename__endswith="_socialnetworklink")
                | Q(codename__endswith="_sponsor")
                | Q(codename__endswith="_staticpagesmodel")
                | Q(codename__endswith="_teammember")
                | Q(codename__endswith="_text")
                | Q(codename__endswith="_title")
                | Q(codename__endswith="_videosblock")
                | Q(codename__endswith="_volunteer")
                | Q(codename__endswith="access_level_2")
            )
            admin_permissions = Permission.objects.all().exclude(
                Q(codename__endswith="access_level_2") | Q(codename__endswith="access_level_1")
            )
            journalist_permissions = Permission.objects.filter(
                Q(codename__endswith="_play") & ~Q(codename__endswith="change_play")
                | Q(codename__endswith="_blogitem") & ~Q(codename__endswith="change_blogitem")
                | Q(codename__endswith="_newsitem") & ~Q(codename__endswith="change_newsitem")
                | Q(codename__endswith="_project") & ~Q(codename__endswith="change_project")
                | Q(codename__endswith="access_level_1")
                | Q(codename__icontains="view_")
            )
            admin_permissions = Permission.objects.all()
            observer_permissions = Permission.objects.filter(Q(codename__icontains="view_"))

            admin, created = Group.objects.get_or_create(name="admin")
            admin.permissions.set(admin_permissions)

            editor, created = Group.objects.get_or_create(name="editor")
            editor.permissions.set(editors_permissions)

            journalist, created = Group.objects.get_or_create(name="journalist")
            journalist.permissions.set(journalist_permissions)

            observer, created = Group.objects.get_or_create(name="observer")
            observer.permissions.set(observer_permissions)

            self.stdout.write(self.style.SUCCESS("Права для пользователей успешно установлены."))
        except CommandError:
            self.stdout.write(self.style.ERROR("Ошибка установки прав."))
