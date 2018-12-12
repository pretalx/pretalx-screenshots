import datetime
from decimal import Decimal

import pytest
import pytz

from django.utils import translation
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from i18nfield.strings import LazyI18nString


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1024x768')
    return chrome_options


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument('headless')
    return firefox_options


# @pytest.yield_fixture(params=["en", "de_DE"], autouse=True)
# def locale(request):
#     from django.conf import settings
#     translation.activate(request.param or settings.LANGUAGE_CODE)
#     yield request.param
#     # TODO: when enabling this again, replace the fixture definitions below with their locale enabled versions


@pytest.fixture
def user():
    # def user(locale):
    locale = 'en'
    from pretalx.person.models import User

    return User.objects.create_user(
        email='john@example.org', name=_('John Doe'), locale=locale, password='john'
    )


@pytest.fixture
def admin_team(organiser, user):
    from pretalx.event.models import Team

    t = Team.objects.create(
        name=_('Organisers'),
        organiser=organiser,
        can_create_events=True,
        can_change_teams=True,
        can_change_organiser_settings=True,
        can_change_event_settings=True,
        can_change_submissions=True,
        is_reviewer=True,
    )
    t.members.add(user)
    return t


@pytest.fixture
def organiser(user):
    # def organiser(user, locale):
    from pretalx.event.models import Organiser

    o = Organiser.objects.create(name=_('Super Organiser'), slug='superorganiser')
    return o


@pytest.fixture
def event(organiser):
    # def event(organiser, locale):
    from pretalx.event.models import Event

    today = datetime.date.today()
    event = Event.objects.create(
        name='Meta Event Tech Alternative',
        is_public=True,
        slug='test',
        email='orga@orga.org',
        date_from=today,
        date_to=today + datetime.timedelta(days=3),
        organiser=organiser,
    )
    # exporting takes quite some time, so this speeds up our tests
    event.settings.export_html_on_schedule_release = False
    event.settings.display_header_pattern = 'topo'
    # if locale in ['en', 'de']:
    #     event.settings.locales = ['en', 'de']
    # else:
    #     event.settings.locales = ['en', locale]
    # event.settings.language = locale
    return event


@pytest.fixture
def client(live_server, selenium, user, admin_team):
    # def client(live_server, selenium, user, admin_team, locale):
    selenium.implicitly_wait(10)
    return selenium


@pytest.fixture
def logged_in_client(live_server, selenium, user, admin_team):
    # def logged_in_client(live_server, selenium, user, admin_team, locale):
    selenium.get(live_server.url + '/orga/login/')
    selenium.implicitly_wait(10)

    selenium.find_element_by_css_selector("form input[name=email]").send_keys(
        user.email
    )
    selenium.find_element_by_css_selector("form input[name=password]").send_keys('john')
    selenium.find_element_by_css_selector("form button[type=submit]").click()
    return selenium


@pytest.fixture
def speaker_question(event):
    from pretalx.submission.models import Question, QuestionVariant

    return Question.objects.create(
        event=event,
        question='Do you have dietary requirements?',
        variant=QuestionVariant.STRING,
        target='speaker',
        required=False,
    )


@pytest.fixture
def submission_question(event):
    from pretalx.submission.models import Question, AnswerOption, QuestionVariant

    question = Question.objects.create(
        event=event,
        question='Which of these will you require for your presentation?',
        variant=QuestionVariant.MULTIPLE,
        target='submission',
        required=False,
    )
    AnswerOption.objects.create(answer='Projector', question=question)
    AnswerOption.objects.create(answer='Sound playback', question=question)
    AnswerOption.objects.create(answer='Presentation laptop', question=question)
    AnswerOption.objects.create(answer='Laser pointer', question=question)
    AnswerOption.objects.create(answer='Assistant', question=question)
    return question


@pytest.fixture
def speaker(event):
    from pretalx.person.models import SpeakerProfile, User

    user = User.objects.create_user(
        password='speakerpwd1!', name='Jane Speaker', email='jane@speaker.org'
    )
    SpeakerProfile.objects.create(
        user=user, event=event, biography='Best speaker in the world.'
    )
    return user


@pytest.fixture
def speaker_client(client, speaker):
    client.force_login(speaker)
    return client


@pytest.fixture
def submission_type(event):
    from pretalx.submission.models import SubmissionType

    return SubmissionType.objects.create(name='Talk', event=event, default_duration=60)


@pytest.fixture
def submission_data(event, submission_type):
    return {
        'title': 'Integrating docker in your devops workflow',
        'submission_type': submission_type,
        'abstract': 'In this talk, I will present the integration of Docker in a variety of devops workflows. We will approach several devops philosophies and see how containerizing environments can improve them.',
        'description': 'I am a leading Docker expert and have worked the last twenty years as a senior devops consultant.',
        'notes': 'My presentation would be better with sound, so if you could provide that, I would be thankful',
        'content_locale': 'en',
        'event': event,
    }


@pytest.fixture
def submission(submission_data, speaker):
    from pretalx.submission.models import Submission

    sub = Submission.objects.create(**submission_data)
    sub.save()
    sub.speakers.add(speaker)
    return sub


@pytest.fixture
def room(event):
    from pretalx.schedule.models import Room

    return Room.objects.create(name=_('Hall 1.01'), event=event)


@pytest.fixture
def other_room(event):
    from pretalx.schedule.models import Room

    return Room.objects.create(name=_('Hall 1.04'), event=event)
