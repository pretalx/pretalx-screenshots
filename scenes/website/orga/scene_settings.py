import pytest

from django.conf import settings


from ...utils import screenshot


@pytest.mark.django_db
def shot_edit_cfp_settings(live_server, event, admin_team, logged_in_client):
    #logged_in_client.get(live_server.url + '/orga/organiser/{}/team/{}'.format(event.organiser.slug, admin_team.pk))
    logged_in_client.get(live_server.url + '/orga/event/{}/cfp/text'.format(event.slug))
    screenshot(logged_in_client, 'website/orga/cfp_settings.png')
