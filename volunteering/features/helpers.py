from __future__ import print_function

from django.core import management
from django.core.wsgi import get_wsgi_application
from django.utils.encoding import smart_text
from django.utils.text import slugify as unicode_slugify

from lettuce import world
from nose.tools import assert_in, assert_not_in
from webtest import TestApp

from dothis.features.helpers import (visit, click, form, submit, body, the,
                                     show_browser)


def setup_session():
    world.browser = TestApp(get_wsgi_application())
    management.call_command('flush', interactive=False)


def teardown_session():
    pass


def visit_the_model_list_page(model_name):
    visit('/admin/volunteering/%s/' % model_name)


def add_a_model(model_name):
    visit_the_model_list_page(model_name)
    click(description='Add')


def set_field_on_admin_page(field, value):
    form()[field] = value


def set_select_field_on_admin_page(field, value):
    form().select(field, text=value)


def set_multi_select_field_on_admin_page(field, value):
    form().select_multiple(field, texts=[value])


def create_campaign(campaign_name, duties=[]):
    show_browser(True)  # for test coverage report
    visit('/admin/volunteering/campaign/')
    click(description='Add')
    form()['name'] = campaign_name
    form()['slug'] = slugify(campaign_name)
    submit()
    for duty in duties:
        duty_name = duty['Name']
        create_duty(duty_name, duty['Attributes'])
        create_campaign_duty(campaign_name, duty_name)


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


def create_duty(duty_name, attribute_names=[]):
    visit('/admin/volunteering/duty/')
    click('Add')
    f = form()
    # f['name'] = duty_name
    # f['slug'] = slugify(duty_name)
    for attribute_name in attribute_names:
        f.select_multiple('attributes', texts=attribute_names)
    submit()


def create_duties(duty_name, attribute_names=[]):
    visit('/admin/volunteering/duty/')
    click('Add')
    f = form()
    # f['name'] = duty_name
    # f['slug'] = slugify(duty_name)
    for attribute_name in attribute_names:
        f.select_multiple('attributes', texts=attribute_names)
    submit()


def create_campaign_duty(campaign_name, duty_name):
    visit('/admin/volunteering/campaignduty/')
    click('Add')
    f = form()
    f.select('campaign', text=campaign_name)
    f.select('duty', text=duty_name)
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


def assert_page_contains(search_string):
    assert_in(search_string, body())


def assert_volunteer_has_available_duties(volunteer, duty_names):
    for name in duty_names:
        assert_in(name, body())


def assert_volunteer_is_assigned_duty(volunteer_name, campaign_name,
                                      duty_name):
    visit_volunteer_duty(volunteer_name, campaign_name, duty_name)
    assert_in("You have volunteered", body())


def assert_volunteer_sees_assigned_duties(volunteer_name, duty_names):
    for name in duty_names:
        assert_in(name, body())


def assert_duty_not_assigned_to_volunteer(volunteer_name, campaign_name,
                                          duty_name):
    visit_volunteer_duty(volunteer_name, campaign_name, duty_name)
    assert_not_in("You have volunteered", body())


def visit_volunteer_duty(volunteer_name, campaign_name, duty_name):
    volunteer = the('Volunteer', name=volunteer_name)
    campaign = the('Campaign', name=campaign_name)
    duty = the('Duty', name=duty_name)
    visit('/volunteering/%s/%s/%s/' % (volunteer.slug, campaign.slug,
                                       duty.slug))


def assert_volunteer_does_not_see_duties(volunteer, duty_names):
    visit('/admin/volunteering/volunteer/%s/' % volunteer.id)
    for name in duty_names:
        assert_not_in(name, body())


def slugify(string):
    return unicode_slugify(smart_text(string))
