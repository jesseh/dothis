# -*- coding: utf-8 -*-

from lettuce import step, before, after
from nose.tools import assert_in

from helpers import (setup_session, teardown_session, login_as_the_admin, body,
                     create_volunteer, create_campaign,
                     assert_campaign_has_duties, the)


@before.each_scenario
def setup(scenario):
    setup_session()


@after.each_scenario
def teardown(scenario):
    teardown_session()


@step(u'^Given a admin user is logged in$')
def given_a_admin_user_is_logged_in(step):
    login_as_the_admin()


@step(u'^Given a coordinator is logged in$')
def given_a_coordinator_is_logged_in(step):
    login_as_the_admin()


@step(u'^When he creates a campaign called "([^"]*)" with duties:$')
def when_he_creates_a_campaign_called_group1_with_duties(step, campaign_name):
    duty_names = [h['Name'] for h in step.hashes]
    create_campaign(campaign_name, duty_names)


@step(u'^Then he sees the "([^"]*)" campaign with the duties:$')
def then_he_sees_the_group1_campaign_with_the_duties(step, campaign_name):
    duty_names = [h['Name'] for h in step.hashes]
    campaign = the('Campaign', name=campaign_name)
    assert_campaign_has_duties(campaign, duty_names)


@step(u'^When he creates a volunteer called "([^"]*)"$')
def when_he_creates_a_volunteer_called_group1(step, volunteer_name):
    create_volunteer(volunteer_name)


@step(u'^Then he sees that the volunteer "([^"]*)" was created$')
def then_he_sees_that_the_volunteer_group1_was_created(step, volunteer_name):
    assert_in(volunteer_name, body())
