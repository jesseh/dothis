from __future__ import print_function

from django.contrib.auth.models import User
from lettuce import world
from nose.tools import assert_in

import volunteering


def the(model_name, **kwargs):
    model = getattr(volunteering.models, model_name)
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
