# -*- coding: utf-8 -*-

from lettuce import step, before
from nose.tools import assert_in

from helpers import (prepare_browser, visit, login_as_the_admin, click, submit,
                     form, body)


@before.all
def set_browser():
    prepare_browser()


@step(u'Given a admin user is logged in')
def given_a_admin_user_is_logged_in(step):
    login_as_the_admin()


@step(u'When he creates a campaign called "([^"]*)"')
def when_he_creates_a_campaign_called_group1(step, campaign_name):
    visit('/admin/campaigns')
    click(description='Add')
    form()['name'] = campaign_name
    submit()


@step(u'Then he sees that the campaign "([^"]*)" was created')
def then_he_sees_that_the_campaign_was_created(step, campaign_name):
    assert_in(campaign_name, body())
