# -*- coding: utf-8 -*-

from lettuce import step, before, after

from helpers import (add_a_model, set_field_on_admin_page, setup_session,
                     teardown_session, create_volunteer, create_attribute,
                     create_campaign, create_duties,
                     set_multi_select_field_on_admin_page,
                     set_select_field_on_admin_page,
                     visit_the_model_list_page, volunteer_for_duty,
                     view_volunteer_plan, assert_page_contains,
                     assert_volunteer_has_available_duties,
                     assert_volunteer_sees_assigned_duties,
                     assert_duty_not_assigned_to_volunteer,
                     assert_volunteer_does_not_see_duties,
                     assert_volunteer_is_assigned_duty)
from dothis.features.helpers import (assert_was_created, login_as_the_admin,
                                     the, submit, show_browser)


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


@step(u'^When he creates a volunteer called "([^"]*)"$')
def when_he_creates_a_volunteer_called_group1(step, volunteer_name):
    create_volunteer(volunteer_name)


@step(u'^Then he sees that the volunteer "([^"]*)" was created$')
def then_he_sees_that_the_volunteer_group1_was_created(step, volunteer_name):
    assert_was_created(volunteer_name)


@step(u'^Given the duties:$')
def given_the_duties(step):
    create_duties(step.hashes)


@step(u'^And a doctor who is qualified for the First Aid duty$')
def and_a_doctor_who_is_qualified_for_the_first_aid_duty(step):
    attribute_name = "doctor"
    create_volunteer("Sam Samson", [attribute_name])


@step(u'^Given some duties are assigned to the volunteer:$')
def given_some_duties_are_assigned_to_the_volunteer(step):
    create_volunteer("Sam Samson")
    volunteer = the('Volunteer', name="Sam Samson")
    duty_names = [h['Name'] for h in step.hashes]
    for duty_name in duty_names:
        duty = the('Duty', name=duty_name)
        duty.assigned_to = volunteer
        duty.save()


@step(u'^Given some duties are assigned to another volunteer:$')
def given_some_duties_are_assigned_to_another_volunteer(step):
    create_volunteer("Other Volunteer")
    volunteer = the('Volunteer', name="Other Volunteer")
    duty_names = [h['Name'] for h in step.hashes]
    for duty_name in duty_names:
        duty = the('Duty', name=duty_name)
        duty.assigned_to = volunteer
        duty.save()


@step(u'^When the volunteer views her plan$')
def when_the_volunteer_views_her_plan(step):
    create_campaign('Summer camp', [{'Name': 'counselor', 'Attributes': ''},
                                    {'Name': 'cook',      'Attributes': ''}])
    view_volunteer_plan("Sam Samson")


@step(u'^Then she sees the available duties for which she could volunteer ' +
      u'to be assigned:$')
def then_she_sees_the_available_duties_for_which_she_could_be_assigned(step):
    volunteer = the('Volunteer', name="Sam Samson")
    duty_names = [h['Name'] for h in step.hashes]
    assert_volunteer_has_available_duties(volunteer, duty_names)


@step(u'^And she sees the duties assigned to her:$')
def and_she_sees_the_duties_assigned_to_her(step):
    volunteer_name = "Sam Samson"
    duty_names = [h['Name'] for h in step.hashes]
    assert_volunteer_sees_assigned_duties(volunteer_name, duty_names)


@step(u'^And she does not sees the duties assigned to others:$')
def and_she_does_not_sees_the_duties_assigned_to_others(step):
    volunteer = the('Volunteer', name="Sam Samson")
    duty_names = [h['Name'] for h in step.hashes]
    assert_volunteer_does_not_see_duties(volunteer, duty_names)


@step(u'^When she creates a attribute called "([^"]*)"$')
def when_she_creates_a_attribute_called_group1(step, attribute_name):
    create_attribute(attribute_name)


@step(u'^Then she sees the "([^"]*)" attribute$')
def then_she_sees_the_group1_attribute(step, attribute_name):
    assert_was_created(attribute_name)


@step(u'^When the doctor volunteers for the previously ' +
      u'unassigned First Aid duty$')
def when_the_doctor_volunteers_for_the_first_aid_duty(step):
    assert_duty_not_assigned_to_volunteer("Sam Samson", "test campaign",
                                          "first aid")
    volunteer_for_duty("Sam Samson", "test campaign", "first aid")


@step(u'^Then the doctor is assigned the First Aid duty$')
def then_the_doctor_is_assigned_the_first_aid_duty(step):
    assert_volunteer_is_assigned_duty("Sam Samson", "test campaign",
                                      "first aid")


@step(u'^When he adds an? "([^"]*)"$')
def when_he_adds_an_model_object(step, model_name):
    add_a_model(model_name)


@step(u'^And sets the "([^"]*)" to be "([^"]*)"$')
def and_sets_the_field_to_be_value(step, field, value):
    set_field_on_admin_page(field, value)


@step(u'^And sets the "([^"]*)" to select "([^"]*)"$')
def and_sets_the_multi_select_to_value(step, field, value):
    set_multi_select_field_on_admin_page(field, value)


@step(u'^And sets the "([^"]*)" to choose "([^"]*)"$')
def and_sets_the_select_field_to_value(step, field, value):
    set_select_field_on_admin_page(field, value)


@step(u'And sets the date to be "([^"]*)"')
def and_sets_the_date_to_be_group1(step, group1):
    assert False, 'This step must be implemented'


@step(u'And submits the form')
def and_submits_the_form(step):
    submit()


@step(u'Then he visits the "([^"]*)" list page')
def then_he_visits_the_group1_list_page(step, model_name):
    visit_the_model_list_page(model_name)


@step(u'And it says "([^"]*)"')
def and_it_says_group1(step, search_string):
    assert_page_contains(search_string)


@step(u'^And it shows the browser$')
def show_the_browser(step):
    show_browser()
