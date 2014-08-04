import unittest
import datetime

from django.db import IntegrityError
from django.test import TestCase

from volunteering.models import (Activity, Assignment, Attribute, Campaign,
                                 Duty, Event, Location, Volunteer)


class TestAttribute(TestCase):
    def testHasAName(self):
        attribute = Attribute(name='yada')
        self.assertEqual('yada', attribute.name)

    def testAttributeIsUnique(self):
        Attribute(name='yada').save()
        with self.assertRaises(Exception):
            Attribute(name='yada').save()


class TestVolunteer(TestCase):
    def testSettingAnAttribute(self):
        v = Volunteer.objects.create(name='tester')
        v.attributes.create(name='attr2')
        self.assertEqual('attr2', v.attributes.all()[0].name)

    def testHasAUniqueSlugThatHas8PlusOneChars(self):
        v = Volunteer.objects.create(name='tester')
        self.assertEqual(9, len(v.slug))

    def testHasSlugWithDashInTheMiddle(self):
        v = Volunteer.objects.create(name='tester')
        self.assertEqual('-', v.slug[4])

    def testTheSlugIsUnique(self):
        v1 = Volunteer.objects.create(name='tester')
        v2 = Volunteer.objects.create(name='tester2')
        self.assertNotEqual(v1.slug, v2.slug)

    def testHasClaimed_IsFalseWhenFalse(self):
        volunteer = Volunteer.objects.create(name='tester')
        duty = Duty.objects.create()
        self.assertFalse(volunteer.has_claimed(duty))

    def testHasClaimed_IsTrueWhenTrue(self):
        volunteer = Volunteer.objects.create(name='tester')
        duty = Duty.objects.create()
        Assignment.objects.create(volunteer=volunteer, duty=duty)
        self.assertTrue(volunteer.has_claimed(duty))


class TestDuty(TestCase):
    @unittest.SkipTest
    def testSettingAnAttribute(self):
        d = Duty.objects.create()
        d.attributes.create(name='attr')
        self.assertEqual('attr', d.attributes.all()[0].name)

    def testHasVolunteerMultiple(self):
        d = Duty(multiple=5)
        self.assertEqual(5, d.multiple)

    def testHasOptionalLocation(self):
        l = Location.objects.create(name="a location")
        d = Duty(location=l)
        self.assertEqual(l.id, d.location_id)

    def testHasOptionalEvent(self):
        e = Event.objects.create(name="a event")
        d = Duty(event=e)
        self.assertEqual(e.id, d.event_id)

    def testDuplicatesEventLocationActivitySet(self):
        e, _ = Event.objects.get_or_create(name="event")
        l, _ = Location.objects.get_or_create(name="location")
        a, _ = Activity.objects.get_or_create(name="activity")
        params = {'event': e, 'location': l, 'activity': a,
                  'start_time': datetime.time(1, 2),
                  'end_time': datetime.time(3, 4)}
        Duty.objects.get_or_create(**params)
        with self.assertRaises(IntegrityError):
            Duty(**params).save()


class TestCampaign(TestCase):
    def testHasSlug(self):
        c = Campaign(slug='a slug')
        self.assertEqual('a slug', c.slug)


class TestAssignment(TestCase):

    def setUp(self):
        self.campaign = Campaign.objects.create(name="a campaign",
                                                slug="a_campaign")
        self.volunteer = Volunteer.objects.create(name='tester')
        self.duty = Duty.objects.create()

    def testHasTimestamps(self):
        assignment = Assignment(volunteer=self.volunteer, duty=self.duty)
        self.assertTrue(assignment.created)
        self.assertTrue(assignment.modified)

    def testNoDuplicates(self):
        Assignment.objects.create(volunteer=self.volunteer, duty=self.duty)
        with self.assertRaises(IntegrityError):
            Assignment.objects.create(volunteer=self.volunteer, duty=self.duty)


class TestActivity(TestCase):
    def setUp(self):
        self.a = Activity(name="the name",
                          description="the short description")

    def testHasAName(self):
        self.assertEqual(self.a.name, 'the name')

    def testNameIsUnique(self):
        self.a.save()
        with self.assertRaises(IntegrityError):
            Activity.objects.create(name='the name')

    def testHasADescription(self):
        self.assertEqual(self.a.description, 'the short description')


class TestEvent(TestCase):
    def setUp(self):
        self.a = Event(name="the name",
                       description="the short description",
                       date=datetime.date(2001, 1, 1))

    def testHasAName(self):
        self.assertEqual(self.a.name, 'the name')

    def testNameIsUnique(self):
        self.a.save()
        with self.assertRaises(IntegrityError):
            Event.objects.create(name='the name')

    def testHasADescription(self):
        self.assertEqual(self.a.description, 'the short description')

    def testHasADate(self):
        self.assertEqual(self.a.date, datetime.date(2001, 1, 1))


class TestLocation(TestCase):
    def setUp(self):
        self.l = Location(name="the name",
                          description="the short description")

    def testHasAName(self):
        self.assertEqual(self.l.name, 'the name')

    def testNameIsUnique(self):
        self.l.save()
        with self.assertRaises(IntegrityError):
            Location.objects.create(name='the name')

    def testHasADescription(self):
        self.assertEqual(self.l.description, 'the short description')
