from datetime import datetime
import factory
from factory.django import DjangoModelFactory

from volunteering.models import (Volunteer, Family, Attribute, Duty, Activity,
                                 Location, Event, Assignment)


class AttributeFactory(DjangoModelFactory):
    class Meta:
        model = Attribute

    name = 'happy'


class FamilyFactory(DjangoModelFactory):
    class Meta:
        model = Family

    external_id = factory.Sequence(lambda n: 'FM{0}'.format(n))


class VolunteerFactory(DjangoModelFactory):
    class Meta:
        model = Volunteer

    first_name = 'Zeb'
    surname = 'Zooler'

    title = 'Mr.'
    first_name = 'Zeb'
    surname = 'Zooler'
    dear_name = ''
    external_id = factory.Sequence(lambda n: 'VR{0}/{0}'.format(n))
    family = factory.SubFactory(FamilyFactory)
    email_address = 'zeb@zebra.net'
    home_phone = '123456'
    mobile_phone = '654321'


class ActivityFactory(DjangoModelFactory):
    class Meta:
        model = Activity
    name = factory.Sequence(lambda n: 'an activity {0}'.format(n))


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event
    name = factory.Sequence(lambda n: 'an event {0}'.format(n))
    date = datetime(2014, 1, 1)


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location
    name = factory.Sequence(lambda n: 'a location {0}'.format(n))


class DutyFactory(DjangoModelFactory):
    class Meta:
        model = Duty


class FullDutyFactory(DjangoModelFactory):
    class Meta:
        model = Duty

    activity = factory.SubFactory(ActivityFactory)
    event = factory.SubFactory(EventFactory)
    location = factory.SubFactory(LocationFactory)


class AssignmentFactory(DjangoModelFactory):
    class Meta:
        model = Assignment

    volunteer = factory.SubFactory(VolunteerFactory)
    duty = factory.SubFactory(DutyFactory)
