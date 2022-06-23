import logging
import random
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError

from apps.afisha.factories import MasterClassFactory, PerformanceFactory, ReadingFactory
from apps.afisha.factories.events import EventFactory
from apps.core.factories import PersonFactory
from apps.core.models import Setting
from apps.feedback.factories import ParticipationApplicationFestivalFactory
from apps.info.factories import (
    FestivalFactory,
    FestivalTeamFactory,
    PartnerFactory,
    PlaceFactory,
    PressReleaseFactory,
    SelectorFactory,
    SponsorFactory,
    VolunteerFactory,
)
from apps.info.models import FestivalTeamMember
from apps.library.factories import AuthorFactory, OtherPlayFactory, PlayFactory, ProgramTypeFactory
from apps.library.factories.constants import YOUTUBE_VIDEO_LINKS
from apps.library.models import Play
from apps.main.factories import BannerFactory as MainBannerFactory
from apps.users.factories import (
    AdminUserFactory,
    EditorUserFactory,
    JournalistUserFactory,
    ObserverUserFactory,
    SuperUserFactory,
)

logging.getLogger("django").setLevel(logging.WARNING)


class FillDbLogsMixin:
    def log_info(self, command, text):
        command.stdout.write()
        command.stdout.write(command.style.SUCCESS(text))
        command.stdout.write()

    def log_success_creation(self, command, obj, obj_verbose_name):
        number = 1
        if isinstance(obj, list):
            number = len(obj)
        text = f"  Успешно создано: {number} {obj_verbose_name}"
        command.stdout.write(command.style.SUCCESS(text))

    def log_error(self, command, text):
        command.stdout.write(command.style.ERROR(text))


class Command(FillDbLogsMixin, BaseCommand):
    help = (
        "Заполняет БД тестовыми данными. Сейчас доступны:"
        " - Пользователь-суперадмин"
        " - Пользователи-админы"
        " - Пользователи-редакторы"
        " - Пользователи-журналисты"
        " - Пользователи-наблюдатели"
        " - Персоны"
        " - Персоны с фотографией"
        " - Персоны с фотографией, городом проживания и email"
        " - Фестивали"
        " - Пресс-релизы"
        " - Волонтёры"
        " - Команда фестиваля"
        " - PR директор"
        " - Попечители"
        " - Партнёры"
        " - Генеральные партнёры"
        " - Отборщики"
        " - Площадки"
        " - Программы"
        " - Авторы"
        " - Пьесы"
        " - Другие пьесы"
        " - Спектакли"
        " - Мастер-классы"
        " - Читки"
        " - События со спектаклем"
        " - События"
        " - Заявки на участие"
        " - Баннеры главной страницы"
    )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:

        try:
            # users creation
            self.log_info(self, "Создаю тестовых пользователей...")

            superuser = SuperUserFactory.create()
            self.log_success_creation(self, superuser, "суперюзер")

            users_admins = AdminUserFactory.create_batch(2)
            self.log_success_creation(self, users_admins, "админов")

            users_editors = EditorUserFactory.create_batch(2)
            self.log_success_creation(self, users_editors, "редакторов")

            users_journalists = JournalistUserFactory.create_batch(2)
            self.log_success_creation(self, users_journalists, "журналистов")

            users_observers = ObserverUserFactory.create_batch(2)
            self.log_success_creation(self, users_observers, "наблюдателя")

            # Core factories
            self.log_info(self, "Создаю общие ресурсы приложений...")

            persons_base = PersonFactory.create_batch(15)
            self.log_success_creation(self, persons_base, "базовых персон")

            persons_with_image = PersonFactory.create_batch(15, add_real_image=True)
            self.log_success_creation(self, persons_with_image, "персон с фото")

            persons_with_image_email_city = PersonFactory.create_batch(
                15,
                add_real_image=True,
                add_email=True,
                add_city=True,
            )
            self.log_success_creation(self, persons_with_image_email_city, "персон с фото, городом, email")

            # Info factories
            self.log_info(self, "Создаю информацию на сайт...")

            festivals = FestivalFactory.create_batch(15)
            self.log_success_creation(self, festivals, "фестивалей")

            press_releases = PressReleaseFactory.create_batch(10)
            self.log_success_creation(self, press_releases, "пресс-релизов")

            volunteers = VolunteerFactory.create_batch(50)
            self.log_success_creation(self, volunteers, "волонтёров")

            teams = FestivalTeamFactory.create_batch(10)
            self.log_success_creation(self, teams, "членов команд")

            pr_director_creation_result, member = self.add_pr_director(self)
            if pr_director_creation_result is False:
                self.log_error(pr_director_creation_result, "Отсутствуют члены команды для создания PR директор")
            else:
                self.log_success_creation(pr_director_creation_result, member, "PR директор")

            sponsors = SponsorFactory.create_batch(10)
            self.log_success_creation(self, sponsors, "попечителей")

            partners = PartnerFactory.create_batch(30)
            self.log_success_creation(self, partners, "партнёров")

            in_footer_partners = PartnerFactory.create_batch(
                5,
                add_real_image=True,
                type="general",
                in_footer_partner=True,
            )
            self.log_success_creation(self, in_footer_partners, "генеральных партнёров")

            selectors = SelectorFactory.create_batch(30)
            self.log_success_creation(self, selectors, "отборщиков")

            places = PlaceFactory.create_batch(3)
            self.log_success_creation(self, places, "площадки")

            # Library factories
            self.log_info(self, "Создаю данные для Библиотеки...")

            programtypes = ProgramTypeFactory.create_batch(3)
            self.log_success_creation(self, programtypes, "программы")

            authors = AuthorFactory.complex_create(25)
            self.log_success_creation(self, authors, "авторов")

            # count of plays depends on 'free' youtube video links, it could be from 50 (at first filldb call) to 0
            plays = self.create_plays(self)
            self.log_success_creation(self, plays, "пьес")

            other_plays = OtherPlayFactory.create_batch(5)
            self.log_success_creation(self, other_plays, "других пьес")

            # Afisha factories
            self.log_info(self, "Создаю данные для Афиши...")

            perfomances = PerformanceFactory.complex_create(10)
            self.log_success_creation(self, perfomances, "спектаклей")

            masterclasses = MasterClassFactory.create_batch(10)
            self.log_success_creation(self, masterclasses, "мастер-классов")

            readings = ReadingFactory.create_batch(10)
            self.log_success_creation(self, readings, "читок")

            events_of_performances = EventFactory.create_batch(5, performance=True)
            self.log_success_creation(self, events_of_performances, "событий спектакля")

            events = EventFactory.create_batch(10)
            self.log_success_creation(self, events, "событий")

            # Other factories
            self.log_info(self, "Создаю баннеры и заявки на участие...")

            participations = ParticipationApplicationFestivalFactory.create_batch(5)
            self.log_success_creation(self, participations, "заявок на участие в фестивале")

            main_banners = MainBannerFactory.create_batch(3, add_real_image=True)
            self.log_success_creation(self, main_banners, "баннера на главную страницу (с картинкой)")

            self.log_info(self, "Создание тестовых данных завершено!")

        except CommandError as err:
            self.log_error(self, f"Ошибка наполнения базы данных:\n{err}")

    def create_plays(self, command):
        def _get_video_links():
            used_links = Play.objects.filter(other_play=False).values_list("url_reading", flat=True)
            return (link for link in YOUTUBE_VIDEO_LINKS if link not in used_links)

        links = _get_video_links()
        for link in links:
            url_reading = random.choice([None, link])
            PlayFactory.create(url_reading=url_reading)
        return links  # needs for notification, because count of Plays is equal to links

    def add_pr_director(self, command):
        member = FestivalTeamMember.objects.filter(team="fest").first()
        if member:
            name = member.person.full_name
            member.is_pr_director = True
            member.save()
            Setting.objects.filter(settings_key="pr_director_name").update(text=name)
            return True, member
        return False, member
