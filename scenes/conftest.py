import datetime
from decimal import Decimal

import pytest
import pytz
from django.utils import translation
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from i18nfield.strings import LazyI18nString


@pytest.yield_fixture(params=["en", "de_DE"], autouse=True)
def locale(request):
    from django.conf import settings
    translation.activate(request.param or settings.LANGUAGE_CODE)
    yield request.param


@pytest.fixture
def user(locale):
    from pretalx.person.models import User
    return User.objects.create_user(email='john@example.org', name=_('John Doe'), locale=locale, password='john')


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
    )
    t.members.add(user)
    return t


@pytest.fixture
def organiser(user, locale):
    from pretalx.event.models import Organiser
    o = Organiser.objects.create(name=_('Super Organiser'), slug='superorganiser')
    return o


@pytest.fixture
def event(organiser, locale):
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
    if locale in ['en', 'de']:
        event.settings.locales = ['en', 'de']
    else:
        event.settings.locales = ['en', locale]
    event.settings.language = locale
    return event


@pytest.fixture
def client(live_server, selenium, user, admin_team, locale):
    selenium.implicitly_wait(10)
    return selenium


@pytest.fixture
def logged_in_client(live_server, selenium, user, admin_team, locale):
    selenium.get(live_server.url + '/orga/login/')
    selenium.implicitly_wait(10)

    selenium.find_element_by_css_selector("form input[name=email]").send_keys(user.email)
    selenium.find_element_by_css_selector("form input[name=password]").send_keys('john')
    selenium.find_element_by_css_selector("form button[type=submit]").click()
    return selenium


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1024x768')
    return chrome_options


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument('headless')
    return firefox_options
