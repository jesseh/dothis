# -*- coding: utf-8 -*-

from lettuce import step, before, after
from nose.tools import assert_in

from helpers import (setup_session, teardown_session, visit,
                     login_as_the_admin, click, submit, form, body)
from campaigns.models import Campaign


@before.each_scenario
def setup(scenario):
    setup_session()


@after.each_scenario
def teardown(scenario):
    teardown_session()


@step(u'^Given a admin user is logged in$')
def given_a_admin_user_is_logged_in(step):
    login_as_the_admin()


@step(u'^When he creates a campaign called "([^"]*)"$')
def when_he_creates_a_campaign_called_group1(step, campaign_name):
    visit('/admin/campaigns/campaign/')
    click(description='Add')
    form()['name'] = campaign_name
    submit()


@step(u'^Given a coordinator is logged in$')
def given_a_coordinator_is_logged_in(step):
    login_as_the_admin()


@step(u'^Then he sees that the campaign "([^"]*)" was created$')
def then_he_sees_that_the_campaign_was_created(step, campaign_name):
    assert_in(campaign_name, body())


@step(u'^When he creates a campaign called "([^"]*)" with duties:$')
def when_he_creates_a_campaign_called_group1_with_duties(step, campaign_name):
    duty_names = [h['Name'] for h in step.hashes]
    visit('/admin/campaigns/campaign/')
    click(description='Add')
    form()['name'] = campaign_name
    for idx, name in enumerate(duty_names):
        form()['duty_set-%s-name' % idx] = name
    submit()


@step(u'^Then he sees the "([^"]*)" campaign with the duties:$')
def then_he_sees_the_group1_campaign_with_the_duties(step, campaign_name):
    duty_names = [h['Name'] for h in step.hashes]

    campaign = Campaign.objects.get(name=campaign_name)
    visit('/admin/campaigns/campaign/%s/' % campaign.id)
    for name in duty_names:
        assert_in(name, body())


@step(u'^When he creates a volunteer called "([^"]*)"$')
def when_he_creates_a_volunteer_called_group1(step, volunteer_name):
    visit('/admin/campaigns/volunteer/')
    click('Add')
    form()['name'] = volunteer_name
    submit()


@step(u'^Then he sees that the volunteer "([^"]*)" was created$')
def then_he_sees_that_the_volunteer_group1_was_created(step, volunteer_name):
    assert_in(volunteer_name, body())
