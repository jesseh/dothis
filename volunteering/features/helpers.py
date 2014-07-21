from __future__ import print_function

from django.core import management
from django.core.wsgi import get_wsgi_application
from lettuce import world
from nose.tools import assert_in, assert_equal, assert_not_in
from webtest import TestApp

from dothis.features.helpers import visit, click, form, submit, body, the


def setup_session():
    world.browser = TestApp(get_wsgi_application())
    management.call_command('flush', interactive=False)


def teardown_session():
    pass


def create_campaign(campaign_name, duties=[]):
    visit('/admin/volunteering/campaign/')
    click(description='Add')
    form()['name'] = campaign_name
    for idx, duty in enumerate(duties):
        form()['duty_set-%s-name' % idx] = duty['Name']
        form()['duty_set-%s-attributes' % idx] = duty['Attributes']
    submit()


def assert_campaign_has_duties(campaign, duties):
    visit('/admin/volunteering/campaign/%s/' % campaign.id)
    for duty in duties:
        assert_in(duty['Name'], body())
        assert_in(duty['Attributes'].replace('"', ''), body())


def create_volunteer(volunteer_name, attribute_names=[]):
    visit('/admin/volunteering/volunteer/')
    click('Add')
    form()['name'] = volunteer_name
    for attribute_name in attribute_names:
        form().select_multiple('attributes', texts=attribute_names)
    submit()


def create_attribute(attribute_name):
    visit('/admin/volunteering/attribute/')
    click('Add')
    form()['name'] = attribute_name
    submit()


def create_duty(duty_name, campaign_name, attribute_names=[]):
    visit('/admin/volunteering/duty/')
    click('Add')
    f = form()
    f['name'] = duty_name
    f.select('campaign', text=campaign_name)
    for attribute_name in attribute_names:
        f.select_multiple('attributes', texts=attribute_names)
    submit()


def view_volunteer_plan(volunteer_name):
    create_campaign('Summer camp', [{'Name': 'counselor', 'Attributes': ''},
                                    {'Name': 'cook',      'Attributes': ''}])

    volunteer = the('Volunteer', name=volunteer_name)
    visit("/admin/volunteering/volunteer/%s/" % volunteer.id)


def assert_volunteer_has_available_duties(volunteer, duty_names):
    visit('/admin/volunteering/volunteer/%s/' % volunteer.id)
    for name in duty_names:
        assert_in(name, body())


def assert_volunteer_is_assigned_duties(volunteer, duty_names):
    assert_equal(set(duty_names),
                 set(volunteer.duty_set.values_list('name', flat=True)))


def assert_volunteer_sees_assigned_duties(volunteer, duty_names):
    visit('/admin/volunteering/volunteer/%s/' % volunteer.id)
    for name in duty_names:
        assert_in(name, body())


def assert_volunteer_is_not_assigned_duties(volunteer, duty_names):
    assert_not_in(set(duty_names),
                  set(volunteer.duty_set.values_list('name', flat=True)))


def assert_volunteer_does_not_see_duties(volunteer, duty_names):
    visit('/admin/volunteering/volunteer/%s/' % volunteer.id)
    for name in duty_names:
        assert_not_in(name, body())
