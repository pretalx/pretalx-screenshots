import pytest

from django.conf import settings
from django_scopes import scope

from ...utils import screenshot


@pytest.mark.django_db
def shot_cfp_submission_info(live_server, event, client):
    with scope(event=event):
        client.get(live_server.url + f'/{event.slug}/submit/423mOn/info/')
    screenshot(client, 'website/cfp_start.png')


@pytest.mark.django_db
def shot_cfp_submission_questions(
    live_server, event, client, submission_question, speaker_question
):
    with scope(event=event):
        client.get(live_server.url + f'/{event.slug}/submit/423mOn/questions/')
    screenshot(client, 'website/cfp_questions.png')
