# -*- coding: utf-8 -*-

from lettuce import *
from lxml import html
from nose.tools import assert_equals, assert_in
from django.core.wsgi import get_wsgi_application
from django.test.client import Client

from lettuce import step
from webtest import TestApp

from django.contrib.auth.models import User

@before.all
def set_browser():
    world.browser = TestApp(get_wsgi_application())

def create_admin_user():
    try:
        return User.objects.get(username='john')
    except User.DoesNotExist:
      user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
      user.is_superuser = True
      user.is_staff = True
      user.save()
      return user

def login_as_admin(user=create_admin_user()):
    response = world.browser.get('/admin/login/').maybe_follow()
    form = response.form
    form['username'] = 'john'
    form['password'] = 'johnpassword'
    response = form.submit('Log in').maybe_follow()
    body = response.body
    assert_in('john', body, "The user 'john' was not logged in.")


@step(u'Given a admin user is logged in')
def given_a_admin_user_is_logged_in(step):
    login_as_admin()

@step(u'When he creates a campaign called "([^"]*)"')
def when_he_creates_a_campaign_called_group1(step, campaign_name):
    response = world.browser.get('/admin/campaigns').maybe_follow()
    response = response.click(description='Add')
    form = response.form
    form['name'] = campaign_name
    response = form.submit().maybe_follow()
    world.last_response = response

@step(u'Then he sees that the campaign "([^"]*)" was created')
def then_he_sees_that_the_campaign_was_created(step, campaign_name):
    body = world.last_response.body
    print(body)
    assert_in(campaign_name, body)

