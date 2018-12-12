import pytest
from datetime import datetime, time

from django.conf import settings

from ...utils import screenshot


@pytest.mark.django_db
def shot_edit_cfp_settings(live_server, event, admin_team, logged_in_client):
    logged_in_client.get(
        live_server.url + '/orga/event/{}/cfp/text#information'.format(event.slug)
    )
    screenshot(logged_in_client, 'website/cfp_settings.png')


@pytest.mark.django_db
def shot_edit_question_settings(live_server, event, admin_team, logged_in_client):
    logged_in_client.get(
        live_server.url + '/orga/event/{}/cfp/questions/new'.format(event.slug)
    )
    logged_in_client.find_element_by_css_selector("#id_variant").click()
    screenshot(logged_in_client, 'website/question_settings.png')


@pytest.mark.django_db
def shot_edit_plugins(live_server, event, admin_team, logged_in_client, user):
    user.is_administrator = True
    user.save()
    logged_in_client.get(
        live_server.url + '/orga/event/{}/settings/plugins'.format(event.slug)
    )
    screenshot(logged_in_client, 'website/plugin_settings.png')


@pytest.mark.django_db
def shot_edit_mail_templates(live_server, event, admin_team, logged_in_client):
    logged_in_client.get(
        live_server.url + '/orga/event/{}/mails/templates'.format(event.slug)
    )
    screenshot(logged_in_client, 'website/mail_templates.png')


@pytest.mark.django_db
def shot_review_submission(
    live_server, event, admin_team, logged_in_client, submission
):
    logged_in_client.get(
        live_server.url
        + '/orga/event/{}/submissions/{}/reviews'.format(event.slug, submission.code)
    )
    screenshot(logged_in_client, 'website/review_submission.png')


@pytest.mark.django_db
def shot_bare_schedule_editor(
    live_server, event, admin_team, logged_in_client, slot, other_submission
):
    logged_in_client.get(
        live_server.url + '/orga/event/{}/schedule/'.format(event.slug)
    )
    logged_in_client.execute_script("""
const selectors = [".alert", ".schedule-header"]
for (selector of selectors) {
    var element = document.querySelector(selector);
    if (element)
        element.parentNode.removeChild(element);
}""")
    screenshot(logged_in_client, 'website/edit_schedule.png')


@pytest.mark.django_db
def shot_export_schedule_editor(
    live_server, event, admin_team, logged_in_client, submission, room, other_room
):
    event.wip_schedule.freeze('v1')
    logged_in_client.get(
        live_server.url + '/orga/event/{}/schedule/export'.format(event.slug)
    )
    screenshot(logged_in_client, 'website/schedule_export.png')
