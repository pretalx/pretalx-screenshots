import pytest
from django_scopes import scope

from ...utils import screenshot


@pytest.mark.django_db
def shot_agenda_public_schedule(live_server, event, client, slot, schedule):
    with scope(event=event):
        client.get(live_server.url + f'/{event.slug}/schedule/')
    screenshot(client, 'website/agenda_public.png')
