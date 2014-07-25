from __future__ import print_function

from django.core import management
from django.core.wsgi import get_wsgi_application
from django.utils.encoding import smart_text
from django.utils.text import slugify as unicode_slugify

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
    form()['slug'] = slugify(campaign_name)
    for idx, duty in enumerate(duties):
        form()['duty_set-%s-name' % idx] = duty['Name']
        form()['duty_set-%s-slug' % idx] = slugify(duty['Name'])
        form()['duty_set-%s-attributes' % idx] = duty['Attributes']
    submit()


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
    f['slug'] = slugify(duty_name)
    f.select('campaign', text=campaign_name)
    for attribute_name in attribute_names:
        f.select_multiple('attributes', texts=attribute_names)
    submit()


def view_volunteer_plan(volunteer_name):
    volunteer = the('Volunteer', name=volunteer_name)
    visit("/volunteering/%s/" % volunteer.slug)


def volunteer_for_duty(volunteer_name, campaign_name, duty_name):
    volunteer = the('Volunteer', name=volunteer_name)
    campaign = the('Campaign', name=campaign_name)
    duty = the('Duty', name=duty_name)
    visit("/volunteering/%s/%s/%s/" % (volunteer.slug, campaign.slug,
                                       duty.slug))
    submit()


def assert_volunteer_has_available_duties(volunteer, duty_names):
    visit('/admin/volunteering/volunteer/%s/' % volunteer.id)
    for name in duty_names:
        assert_in(name, body())


def assert_volunteer_is_assigned_duties(volunteer_name, duty_names):
    volunteer = the('Volunteer', name="Sam Samson")
    assert_equal(set(duty_names),
                 set(volunteer.duty_set.values_list('name', flat=True)))


def assert_volunteer_is_assigned_duty(volunteer_name, campaign_name, duty_name):
    volunteer = the('Volunteer', name=volunteer_name)
    campaign = the('Campaign', name=campaign_name)
    duty = the('Duty', name=duty_name)
    visit('/volunteering/%s/%s/%s/' % (volunteer.slug, campaign.slug, duty.slug))
    assert_in("Assigned to %s" % volunteer.name, body())


def assert_volunteer_sees_assigned_duties(volunteer_name, duty_names):
    volunteer = the('Volunteer', name="Sam Samson")
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


def slugify(string):
    return unicode_slugify(smart_text(string))
