from datetime import date
import factory
from factory.django import DjangoModelFactory

from volunteering.models import (Volunteer, Family, Attribute, Duty, Activity,
                                 Location, Event, Assignment, Campaign,
                                 Message, Trigger, Sendable)


class AttributeFactory(DjangoModelFactory):
    class Meta:
        model = Attribute

    name = factory.Sequence(lambda n: 'an attribute {0}'.format(n))


class FamilyFactory(DjangoModelFactory):
    class Meta:
        model = Family

    external_id = factory.Sequence(lambda n: 'FM{0}'.format(n))


class VolunteerFactory(DjangoModelFactory):
    class Meta:
        model = Volunteer

    title = 'Mr.'
    first_name = 'Zeb'
    surname = factory.Sequence(lambda n: 'Zooler{0}'.format(n))
    dear_name = 'Zeb'
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
    date = date(2014, 1, 1)


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


class CampaignFactory(DjangoModelFactory):
    class Meta:
        model = Campaign

    name = factory.Sequence(lambda n: 'a campaign {0}'.format(n))
    slug = factory.Sequence(lambda n: 'slug{0}'.format(n))


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    name = factory.Sequence(lambda n: 'a message {0}'.format(n))
    subject = factory.Sequence(lambda n: 'message subjet {0}'.format(n))
    body = factory.Sequence(lambda n: 'message body {0}'.format(n))


class TriggerFactory(DjangoModelFactory):
    class Meta:
        model = Trigger

    campaign = factory.SubFactory(CampaignFactory)
    message = factory.SubFactory(MessageFactory)
    fixed_date = date.today()


class SendableFactory(DjangoModelFactory):
    class Meta:
        model = Sendable

    trigger = factory.SubFactory(TriggerFactory)
    volunteer = factory.SubFactory(VolunteerFactory)
    send_date = date.today()


class SendableAssignmentFactory(SendableFactory):
    assignment = factory.SubFactory(AssignmentFactory)
