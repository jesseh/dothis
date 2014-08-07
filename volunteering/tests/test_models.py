import unittest
from datetime import date, time

from django.db import IntegrityError
from django.test import TestCase

from factories import (AttributeFactory, VolunteerFactory, FamilyFactory,
                       DutyFactory, FullDutyFactory, EventFactory,
                       LocationFactory, ActivityFactory, AssignmentFactory,
                       CampaignFactory, SendableFactory,
                       SendableAssignmentFactory, TriggerFactory)

from volunteering.models import (Activity, Assignment, Attribute, Campaign,
                                 Duty, Event, Location, Sendable, Trigger)


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
        a_time = time(10, 0)
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
        duty2 = FullDutyFactory()
        duty3 = FullDutyFactory()
        duty4 = FullDutyFactory()
        campaign.events.add(duty1.event)
        campaign.events.add(duty2.event)
        campaign.events.add(duty3.event)
        campaign.events.add(duty4.event)

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

        qs = campaign.recipients(True, True).order_by('id')
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

        qs = campaign.recipients(True, True).order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer)])

    def testRecipientsViaAssigned(self):
        campaign = CampaignFactory()
        duty = FullDutyFactory()
        campaign.events.add(duty.event)

        volunteer = VolunteerFactory()
        AssignmentFactory(duty=duty, volunteer=volunteer)

        qs = campaign.recipients(assigned=True).order_by('id')
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
        campaign.activities.add(duty2.activity)

        volunteer2 = VolunteerFactory()
        AssignmentFactory(duty=duty2, volunteer=volunteer2)

        qs = campaign.recipients(True, True).order_by('id')
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

        expected = "<ul><li>%s - %s</li><li>%s - %s</li></ul>" % (
            volunteer2.name(), volunteer2.email_address,
            volunteer1.name(), volunteer1.email_address)

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
                       date=date(2001, 1, 1))

    def testHasAName(self):
        self.assertEqual(self.a.name, 'the name')

    def testNameIsUnique(self):
        self.a.save()
        with self.assertRaises(IntegrityError):
            Event.objects.create(name='the name')

    def testHasADescription(self):
        self.assertEqual(self.a.description, 'the short description')

    def testHasADate(self):
        self.assertEqual(self.a.date, date(2001, 1, 1))


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


class TestSendable(TestCase):
    def testSendableFactory(self):
        s = SendableFactory()
        self.assertTrue(Sendable.objects.filter(pk=s.pk).exists())

    def testSendableAssignmentFactory(self):
        s = SendableAssignmentFactory()
        self.assertTrue(Sendable.objects.filter(pk=s.pk).exists())

    def testSendable_CollectSendablesAssignable(self):
        fix_to_date = date(2005, 5, 5)
        c = CampaignFactory()
        d = FullDutyFactory()
        c.events.add(d.event)
        v = VolunteerFactory()
        a = AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        TriggerFactory.create_batch(3, fixed_date=fix_to_date,
                                    fixed_assignment_state=Trigger.ASSIGNABLE,
                                    campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(3, len(result))
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [v, v, v],
                                 transform=lambda s: s.volunteer)

    def testSendable_CollectSendablesAssignableButAlreadyAssigned(self):
        fix_to_date = date(2005, 5, 5)
        c = CampaignFactory()
        d = FullDutyFactory()
        c.events.add(d.event)
        v = VolunteerFactory()
        a = AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        AssignmentFactory(volunteer=v, duty=d)
        TriggerFactory.create(fixed_date=fix_to_date,
                              fixed_assignment_state=Trigger.ASSIGNABLE,
                              campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(0, len(result))
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [])

    def testSendable_CollectSendablesAssigned(self):
        fix_to_date = date(2005, 5, 5)
        c = CampaignFactory()
        d = FullDutyFactory()
        c.events.add(d.event)
        v = VolunteerFactory()
        a = AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        TriggerFactory.create_batch(3, fixed_date=fix_to_date,
                                    fixed_assignment_state=Trigger.ASSIGNED,
                                    campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(0, len(result))
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [])


class TestTrigger(TestCase):
    def testTriggerFactory(self):
        t = TriggerFactory()
        self.assertTrue(Trigger.objects.filter(id=t.id).exists())

    def testGetFixedDateTriggersSetForADateAllAssignmentStates(self):
        fix_to_date = date(2005, 5, 5)
        triggers = TriggerFactory.create_batch(3, fixed_date=fix_to_date)
        TriggerFactory(fixed_date=date(2001, 1, 1))
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])

    def testGetFixedDateTriggersSetForADateAssignedWithNoAssigned(self):
        fix_to_date = date(2005, 5, 5)
        TriggerFactory.create_batch(3, fixed_date=fix_to_date,
                                    fixed_assignment_state=Trigger.ASSIGNED)
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [])

    def testGetFixedDateTriggersSetForADateAssignedWithAssigned(self):
        fix_to_date = date(2005, 5, 5)
        d = FullDutyFactory()
        c = CampaignFactory()
        c.events.add(d.event)
        v = VolunteerFactory()
        AssignmentFactory(volunteer=v, duty=d)
        triggers = TriggerFactory.create_batch(
            3, fixed_date=fix_to_date, fixed_assignment_state=Trigger.ASSIGNED,
            campaign=c)
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])

    # Skipped until I figure out how to use annotations for this.
    # def testGetFixedDateTriggersSetForADateAssignableWithAssigned(self):
    #     fix_to_date = date(2005, 5, 5)
    #     d = FullDutyFactory()
    #     c = CampaignFactory()
    #     c.events.add(d.event)
    #     v = VolunteerFactory()
    #     AssignmentFactory(volunteer=v, duty=d)
    #     TriggerFactory.create_batch(3, fixed_date=fix_to_date,
    #                                 fixed_assignment_state=Trigger.ASSIGNABLE,
    #                                 campaign=c)
    #     result = Trigger.objects.triggered(fix_to_date).order_by('id')
    #     self.assertQuerysetEqual(result, [])

    def testGetFixedDateTriggersSetForADateAssignableWithAssignable(self):
        fix_to_date = date(2005, 5, 5)
        c = CampaignFactory()
        d = FullDutyFactory()
        c.events.add(d.event)
        v = VolunteerFactory()
        a = AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        AssignmentFactory(volunteer=v, duty=d)
        triggers = TriggerFactory.create_batch(
            3, fixed_date=fix_to_date,
            fixed_assignment_state=Trigger.ASSIGNABLE, campaign=c)
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])
