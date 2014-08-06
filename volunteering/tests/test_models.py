import unittest
import datetime

from django.db import IntegrityError
from django.test import TestCase

from factories import (AttributeFactory, VolunteerFactory, FamilyFactory,
                       DutyFactory, FullDutyFactory, EventFactory,
                       LocationFactory, ActivityFactory, AssignmentFactory,
                       CampaignFactory)

from volunteering.models import (Activity, Assignment, Attribute, Campaign,
                                 Duty, Event, Location)


class TestAttribute(TestCase):
    def testHasAName(self):
        attribute = Attribute(name='yada')
        self.assertEqual('yada', attribute.name)

    def testAttributeIsUnique(self):
        AttributeFactory.create(name='yada')
        with self.assertRaises(Exception):
            AttributeFactory.create(name='yada')


class TestVolunteer(TestCase):
    def testSettingAnAttribute(self):
        v = VolunteerFactory.create(surname='tester')
        a = AttributeFactory.create(name='an attr')
        v.attributes.add(a)
        self.assertEqual('an attr', v.attributes.all()[0].name)

    def testHasAUniqueSlugThatHas8PlusOneChars(self):
        v = VolunteerFactory.create()
        self.assertEqual(9, len(v.slug))

    def testHasSlugWithDashInTheMiddle(self):
        v = VolunteerFactory.create()
        self.assertEqual('-', v.slug[4])

    def testTheSlugIsUnique(self):
        v1 = VolunteerFactory.build()
        v2 = VolunteerFactory.build()
        f = FamilyFactory.create()
        self.assertEqual('', v1.slug)
        self.assertEqual('', v2.slug)
        v1.family = f
        v2.family = f
        v1.save()
        v2.save()
        self.assertNotEqual(v1.slug, v2.slug)

    def testInitials(self):
        volunteer = VolunteerFactory(first_name="Jon", surname="George")
        self.assertEqual('J.G.', volunteer.initials())

    def testInitialsMultipleLastName(self):
        volunteer = VolunteerFactory(first_name="Jon Smith", surname="Stuart")
        self.assertEqual('J.S.', volunteer.initials())

    def testFamilyLink(self):
        volunteer = VolunteerFactory()
        self.assertRegexpMatches(
            volunteer.family_link(),
            '<a href="/admin/volunteering/family/\d*/">FM\d*</a>')

    def testHasClaimed_IsFalseWhenFalse(self):
        volunteer = VolunteerFactory()
        duty = DutyFactory()
        self.assertFalse(volunteer.has_claimed(duty))

    def testHasClaimed_IsTrueWhenTrue(self):
        volunteer = VolunteerFactory.create()
        duty = DutyFactory()
        Assignment.objects.create(volunteer=volunteer, duty=duty)
        self.assertTrue(volunteer.has_claimed(duty))


class TestDuty(TestCase):
    @unittest.SkipTest
    def testSettingAnAttribute(self):
        d = DutyFactory()
        a = AttributeFactory(name='attr')
        d.attributes.add(a)
        self.assertEqual('attr', d.attributes.all()[0].name)

    def testHasVolunteerMultiple(self):
        d = DutyFactory.build(multiple=5)
        self.assertEqual(5, d.multiple)

    def testHasOptionalLocation(self):
        l = LocationFactory.build(name="a location")
        d = DutyFactory.build(location=l)
        self.assertEqual(l.id, d.location_id)

    def testHasOptionalEvent(self):
        e = EventFactory(name="a event")
        d = DutyFactory(event=e)
        self.assertEqual(e.id, d.event_id)

    def testDuplicatesEventLocationActivitySet(self):
        a_time = datetime.time(10, 0)
        d = FullDutyFactory.create(start_time=a_time, end_time=a_time)
        with self.assertRaises(IntegrityError):
            Duty(activity=d.activity, location=d.location, event=d.event,
                 start_time=d.start_time, end_time=d.end_time).save()

    def testOneOfOneIsAssignable(self):
        DutyFactory.create()
        self.assertEqual(1, Duty.objects.assignable().count())

    def testNoneIsAssignable(self):
        DutyFactory.create(multiple=0)
        self.assertEqual(0, Duty.objects.assignable().count())

    def testOneIsAlreadyAssigned(self):
        d = DutyFactory.create(multiple=1)
        AssignmentFactory(duty=d)
        self.assertEqual(0, Duty.objects.assignable().count())

    def testOneIsAlreadyAssignedOfTwo(self):
        d = DutyFactory.create(multiple=2)
        AssignmentFactory(duty=d)
        self.assertEqual(1, Duty.objects.assignable().count())


class TestCampaign(TestCase):
    def testHasSlug(self):
        c = Campaign(slug='a slug')
        self.assertEqual('a slug', c.slug)

    def testDuties(self):
        campaign = CampaignFactory()
        duty1 = FullDutyFactory()
        campaign.activities.add(duty1.activity)
        duty2 = FullDutyFactory()
        campaign.locations.add(duty2.location)
        duty3 = FullDutyFactory()
        campaign.events.add(duty3.event)
        duty4 = FullDutyFactory()
        campaign.events.add(duty4.event)
        campaign.locations.add(duty4.location)

        qs = campaign.duties().order_by('id')
        expected = [duty1, duty2, duty3, duty4]
        self.assertQuerysetEqual(qs, [repr(d) for d in expected])

    def testRecipientsViaAssignable(self):
        campaign = CampaignFactory()
        attribute = AttributeFactory()
        duty1 = FullDutyFactory()
        duty1.activity.attributes.add(attribute)
        volunteer = VolunteerFactory()
        volunteer.attributes.add(attribute)
        campaign.activities.add(duty1.activity)

        qs = campaign.recipients().order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer)])

    def testRecipientsViaAssignableTwice(self):
        campaign = CampaignFactory()
        attribute = AttributeFactory()
        duty1 = FullDutyFactory()
        duty1.activity.attributes.add(attribute)
        duty2 = FullDutyFactory()
        duty2.activity.attributes.add(attribute)
        volunteer = VolunteerFactory()
        volunteer.attributes.add(attribute)
        campaign.activities.add(duty1.activity)
        campaign.events.add(duty2.event)

        qs = campaign.recipients().order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer)])

    def testRecipientsViaAssigned(self):
        campaign = CampaignFactory()
        duty = FullDutyFactory()
        campaign.events.add(duty.event)

        volunteer = VolunteerFactory()
        AssignmentFactory(duty=duty, volunteer=volunteer)

        qs = campaign.recipients().order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer)])

    def testRecipientsViaAssignedAndAssignable(self):
        campaign = CampaignFactory()

        attribute = AttributeFactory()
        duty1 = FullDutyFactory()
        duty1.activity.attributes.add(attribute)
        campaign.activities.add(duty1.activity)

        volunteer1 = VolunteerFactory()
        volunteer1.attributes.add(attribute)

        duty2 = FullDutyFactory()
        campaign.events.add(duty2.event)

        volunteer2 = VolunteerFactory()
        AssignmentFactory(duty=duty2, volunteer=volunteer2)

        qs = campaign.recipients().order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer1), repr(volunteer2)])

    def testRecipientsCount(self):
        campaign = CampaignFactory()
        duty = FullDutyFactory()
        campaign.events.add(duty.event)

        volunteer = VolunteerFactory()
        AssignmentFactory(duty=duty, volunteer=volunteer)

        self.assertEqual(1, campaign.recipient_count())

    def testRecipientNames(self):
        campaign = CampaignFactory()
        duty = FullDutyFactory()
        campaign.events.add(duty.event)

        volunteer1 = VolunteerFactory()
        AssignmentFactory(duty=duty, volunteer=volunteer1)
        volunteer2 = VolunteerFactory(first_name='Abe')
        AssignmentFactory(duty=duty, volunteer=volunteer2)

        expected = "<ul><li>%s</li><li>%s</li></ul>" % (volunteer2.name(),
                                                        volunteer1.name())

        self.assertEqual(expected, campaign.recipient_names())


class TestAssignment(TestCase):

    def setUp(self):
        self.volunteer = VolunteerFactory.create()
        self.duty = Duty.objects.create()

    def testHasTimestamps(self):
        assignment = Assignment(volunteer=self.volunteer, duty=self.duty)
        self.assertTrue(assignment.created)
        self.assertTrue(assignment.modified)

    def testNoDuplicates(self):
        AssignmentFactory.create(volunteer=self.volunteer, duty=self.duty)
        with self.assertRaises(IntegrityError):
            AssignmentFactory.create(volunteer=self.volunteer, duty=self.duty)


class TestActivity(TestCase):
    def setUp(self):
        self.a = ActivityFactory.build(name="the name",
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


class TestFamily(TestCase):
    def testSingleSurnames(self):
        v = VolunteerFactory(surname="Abba")
        family = v.family
        self.assertEqual("Abba", family.surnames())

    def testMultipleSurnames(self):
        v = VolunteerFactory(surname="Abba")
        family = v.family
        VolunteerFactory(family=family, surname="Bacca")
        self.assertEqual('Abba, Bacca', family.surnames())

    def testSingleNames(self):
        v = VolunteerFactory(first_name="Joe", surname="Abba")
        family = v.family
        self.assertEqual("Joe Abba", family.names())

    def testMultipleNames(self):
        v = VolunteerFactory(first_name="Joe", surname="Abba")
        family = v.family
        VolunteerFactory(family=family, first_name="Bob", surname="Bacca")
        self.assertEqual('Bob Bacca, Joe Abba', family.names())
