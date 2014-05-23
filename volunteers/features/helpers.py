from dothis.features.helpers import (visit, click, form, submit)


def create_volunteer(volunteer_name):
    visit('/admin/volunteers/volunteer/')
    click('Add')
    form()['name'] = volunteer_name
    submit()
