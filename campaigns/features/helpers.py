from __future__ import print_function

from django.contrib.auth.models import User
from django.core import management
from django.core.wsgi import get_wsgi_application
from lettuce import world
from nose.tools import assert_in
from webtest import TestApp

import campaigns


def setup_session():
    world.browser = TestApp(get_wsgi_application())
    management.call_command('flush', interactive=False)


def teardown_session():
    pass


def the(model_name, **kwargs):
    model = getattr(campaigns.models, model_name)
    return model.objects.get(**kwargs)


def page():
    return world.last_response


def set_page(response):
    world.last_response = response


def visit(url):
    set_page(world.browser.get(url).maybe_follow())


def click(description):
    set_page(page().click(description=description).maybe_follow())


def form():
    return page().form


def submit():
    set_page(form().submit().maybe_follow())


def body():
    return page().body


def create_the_admin_user():
    try:
        return User.objects.get(username='johntheadmin')
    except User.DoesNotExist:
        user = User.objects.create_user('johntheadmin',
                                        'lennon@thebeatles.com',
                                        'johnpassword')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


def login_as_the_admin(user=None):
    if user is None:
        user = create_the_admin_user()
    visit('/admin/login/')
    form()['username'] = 'johntheadmin'
    form()['password'] = 'johnpassword'
    submit()
    assert_in('john', body(), "The user 'john' was not logged in.")


def create_campaign(campaign_name, duty_names=[]):
    visit('/admin/campaigns/campaign/')
    click(description='Add')
    form()['name'] = campaign_name
    for idx, name in enumerate(duty_names):
        form()['duty_set-%s-name' % idx] = name
    submit()


def create_volunteer(volunteer_name):
    visit('/admin/campaigns/volunteer/')
    click('Add')
    form()['name'] = volunteer_name
    submit()


def assert_campaign_has_duties(campaign, duty_names):
    visit('/admin/campaigns/campaign/%s/' % campaign.id)
    for name in duty_names:
        assert_in(name, body())
