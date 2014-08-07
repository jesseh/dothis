import unittest
from datetime import date, time

from django.db import IntegrityError
from django.test import TestCase

import factories as f

from volunteering.models import (Activity, Assignment, Attribute, Campaign,
                                 Duty, Event, Location, Sendable, Trigger,
                                 Message)


class TestAttribute(TestCase):
    def testHasAName(self):
        attribute = Attribute(name='yada')
        self.assertEqual('yada', attribute.name)

    def testAttributeIsUnique(self):
        f.AttributeFactory.create(name='yada')
        with self.assertRaises(Exception):
            f.AttributeFactory.create(name='yada')


class TestVolunteer(TestCase):
    def testSettingAnAttribute(self):
        v = f.VolunteerFactory.create(surname='tester')
        a = f.AttributeFactory.create(name='an attr')
        v.attributes.add(a)
        self.assertEqual('an attr', v.attributes.all()[0].name)

    def testHasAUniqueSlugThatHas8PlusOneChars(self):
        v = f.VolunteerFactory.create()
        self.assertEqual(9, len(v.slug))

    def testHasSlugWithDashInTheMiddle(self):
        v = f.VolunteerFactory.create()
        self.assertEqual('-', v.slug[4])

    def testTheSlugIsUnique(self):
        v1 = f.VolunteerFactory.build()
        v2 = f.VolunteerFactory.build()
        fam = f.FamilyFactory.create()
        self.assertEqual('', v1.slug)
        self.assertEqual('', v2.slug)
        v1.family = fam
        v2.family = fam
        v1.save()
        v2.save()
        self.assertNotEqual(v1.slug, v2.slug)

    def testInitials(self):
        volunteer = f.VolunteerFactory(first_name="Jon", surname="George")
        self.assertEqual('J.G.', volunteer.initials())

    def testFormalName(self):
        volunteer = f.VolunteerFactory(first_name="", dear_name="",
                                       surname="Smith", title="Mr.")
        self.assertEqual('Mr. Smith', volunteer.formal_name())

    def testFormalName_NoTitle(self):
        volunteer = f.VolunteerFactory(first_name="", dear_name="",
                                       surname="Smith", title="")
        self.assertEqual('Smith', volunteer.formal_name())

    def testToName_WithDearName(self):
        volunteer = f.VolunteerFactory(first_name="Jon", dear_name="Sam")
        self.assertEqual('Sam', volunteer.to_name())

    def testToName_WithNoDearName(self):
        volunteer = f.VolunteerFactory(first_name="Jon", dear_name="")
        self.assertEqual('Jon', volunteer.to_name())

    def testToName_WithNoDearNameNorTitle(self):
        volunteer = f.VolunteerFactory(first_name="", dear_name="",
                                       surname="Smith", title="Mr.")
        self.assertEqual('Mr. Smith', volunteer.to_name())

    def testInitialsMultipleLastName(self):
        volunteer = f.VolunteerFactory(first_name="Jon Smith",
                                       surname="Stuart")
        self.assertEqual('J.S.', volunteer.initials())

    def testFamilyLink(self):
        volunteer = f.VolunteerFactory()
        self.assertRegexpMatches(
            volunteer.family_link(),
            '<a href="/admin/volunteering/family/\d*/">FM\d*</a>')

    def testHasClaimed_IsFalseWhenFalse(self):
        volunteer = f.VolunteerFactory()
        duty = f.DutyFactory()
        self.assertFalse(volunteer.has_claimed(duty))

    def testHasClaimed_IsTrueWhenTrue(self):
        volunteer = f.VolunteerFactory.create()
        duty = f.DutyFactory()
        Assignment.objects.create(volunteer=volunteer, duty=duty)
        self.assertTrue(volunteer.has_claimed(duty))


class TestDuty(TestCase):
    @unittest.SkipTest
    def testSettingAnAttribute(self):
        d = f.DutyFactory()
        a = f.AttributeFactory(name='attr')
        d.attributes.add(a)
        self.assertEqual('attr', d.attributes.all()[0].name)

    def testHasVolunteerMultiple(self):
        d = f.DutyFactory.build(multiple=5)
        self.assertEqual(5, d.multiple)

    def testHasOptionalLocation(self):
        l = f.LocationFactory.build(name="a location")
        d = f.DutyFactory.build(location=l)
        self.assertEqual(l.id, d.location_id)

    def testHasOptionalEvent(self):
        e = f.EventFactory(name="a event")
        d = f.DutyFactory(event=e)
        self.assertEqual(e.id, d.event_id)

    def testDuplicatesEventLocationActivitySet(self):
        a_time = time(10, 0)
        d = f.FullDutyFactory.create(start_time=a_time, end_time=a_time)
        with self.assertRaises(IntegrityError):
            Duty(activity=d.activity, location=d.location, event=d.event,
                 start_time=d.start_time, end_time=d.end_time).save()

    def testOneOfOneIsAssignable(self):
        f.DutyFactory.create()
        self.assertEqual(1, Duty.objects.assignable().count())

    def testNoneIsAssignable(self):
        f.DutyFactory.create(multiple=0)
        self.assertEqual(0, Duty.objects.assignable().count())

    def testOneIsAlreadyAssigned(self):
        d = f.DutyFactory.create(multiple=1)
        f.AssignmentFactory(duty=d)
        self.assertEqual(0, Duty.objects.assignable().count())

    def testOneIsAlreadyAssignedOfTwo(self):
        d = f.DutyFactory.create(multiple=2)
        f.AssignmentFactory(duty=d)
        self.assertEqual(1, Duty.objects.assignable().count())


class TestCampaign(TestCase):
    def testHasSlug(self):
        c = Campaign(slug='a slug')
        self.assertEqual('a slug', c.slug)

    def testDuties(self):
        campaign = f.CampaignFactory()
        duty1 = f.FullDutyFactory()
        duty2 = f.FullDutyFactory()
        duty3 = f.FullDutyFactory()
        duty4 = f.FullDutyFactory()
        campaign.events.add(duty1.event)
        campaign.events.add(duty2.event)
        campaign.events.add(duty3.event)
        campaign.events.add(duty4.event)

        qs = campaign.duties().order_by('id')
        expected = [duty1, duty2, duty3, duty4]
        self.assertQuerysetEqual(qs, [repr(d) for d in expected])

    def testRecipientsViaAssignable(self):
        campaign = f.CampaignFactory()
        attribute = f.AttributeFactory()
        duty1 = f.FullDutyFactory()
        duty1.activity.attributes.add(attribute)
        volunteer = f.VolunteerFactory()
        volunteer.attributes.add(attribute)
        campaign.activities.add(duty1.activity)

        qs = campaign.recipients(True, True).order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer)])

    def testRecipientsViaAssignableTwice(self):
        campaign = f.CampaignFactory()
        attribute = f.AttributeFactory()
        duty1 = f.FullDutyFactory()
        duty1.activity.attributes.add(attribute)
        duty2 = f.FullDutyFactory()
        duty2.activity.attributes.add(attribute)
        volunteer = f.VolunteerFactory()
        volunteer.attributes.add(attribute)
        campaign.activities.add(duty1.activity)

        qs = campaign.recipients(True, True).order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer)])

    def testRecipientsViaAssigned(self):
        campaign = f.CampaignFactory()
        duty = f.FullDutyFactory()
        campaign.events.add(duty.event)

        volunteer = f.VolunteerFactory()
        f.AssignmentFactory(duty=duty, volunteer=volunteer)

        qs = campaign.recipients(assigned=True).order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer)])

    def testRecipientsViaAssignedAndAssignable(self):
        campaign = f.CampaignFactory()

        attribute = f.AttributeFactory()
        duty1 = f.FullDutyFactory()
        duty1.activity.attributes.add(attribute)
        campaign.activities.add(duty1.activity)

        volunteer1 = f.VolunteerFactory()
        volunteer1.attributes.add(attribute)

        duty2 = f.FullDutyFactory()
        campaign.activities.add(duty2.activity)

        volunteer2 = f.VolunteerFactory()
        f.AssignmentFactory(duty=duty2, volunteer=volunteer2)

        qs = campaign.recipients(True, True).order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer1), repr(volunteer2)])

    def testRecipientsCount(self):
        campaign = f.CampaignFactory()
        duty = f.FullDutyFactory()
        campaign.events.add(duty.event)

        volunteer = f.VolunteerFactory()
        f.AssignmentFactory(duty=duty, volunteer=volunteer)

        self.assertEqual(1, campaign.recipient_count())

    def testRecipientNames(self):
        campaign = f.CampaignFactory()
        duty = f.FullDutyFactory()
        campaign.events.add(duty.event)

        volunteer1 = f.VolunteerFactory()
        f.AssignmentFactory(duty=duty, volunteer=volunteer1)
        volunteer2 = f.VolunteerFactory(first_name='Abe')
        f.AssignmentFactory(duty=duty, volunteer=volunteer2)

        expected = "<ul><li>%s - %s</li><li>%s - %s</li></ul>" % (
            volunteer2.name(), volunteer2.email_address,
            volunteer1.name(), volunteer1.email_address)

        self.assertEqual(expected, campaign.recipient_names())


class TestAssignment(TestCase):

    def setUp(self):
        self.volunteer = f.VolunteerFactory.create()
        self.duty = Duty.objects.create()

    def testHasTimestamps(self):
        assignment = Assignment(volunteer=self.volunteer, duty=self.duty)
        self.assertTrue(assignment.created)
        self.assertTrue(assignment.modified)

    def testNoDuplicates(self):
        f.AssignmentFactory.create(volunteer=self.volunteer, duty=self.duty)
        with self.assertRaises(IntegrityError):
            f.AssignmentFactory.create(volunteer=self.volunteer,
                                       duty=self.duty)


class TestActivity(TestCase):
    def setUp(self):
        self.a = f.ActivityFactory.build(
            name="the name", description="the short description")

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
        v = f.VolunteerFactory(surname="Abba")
        family = v.family
        self.assertEqual("Abba", family.surnames())

    def testMultipleSurnames(self):
        v = f.VolunteerFactory(surname="Abba")
        family = v.family
        f.VolunteerFactory(family=family, surname="Bacca")
        self.assertEqual('Abba, Bacca', family.surnames())

    def testSingleNames(self):
        v = f.VolunteerFactory(first_name="Joe", surname="Abba")
        family = v.family
        self.assertEqual("Joe Abba", family.names())

    def testMultipleNames(self):
        v = f.VolunteerFactory(first_name="Joe", surname="Abba")
        family = v.family
        f.VolunteerFactory(family=family, first_name="Bob", surname="Bacca")
        self.assertEqual('Bob Bacca, Joe Abba', family.names())


class TestSendable(TestCase):
    def testSendableFactory(self):
        s = f.SendableFactory()
        self.assertTrue(Sendable.objects.filter(pk=s.pk).exists())

    def testSendableAssignmentFactory(self):
        s = f.SendableAssignmentFactory()
        self.assertTrue(Sendable.objects.filter(pk=s.pk).exists())

    def testSendable_CollectSendablesAssignable(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.TriggerFactory.create_batch(
            3, fixed_date=fix_to_date,
            fixed_assignment_state=Trigger.ASSIGNABLE, campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(3, result)
        all_qs = Sendable.objects.all().order_by('id')
        self.assertQuerysetEqual(all_qs, [v, v, v],
                                 transform=lambda s: s.volunteer)

    def testSendable_CollectSendablesAssignableButAlreadyAssigned(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.AssignmentFactory(volunteer=v, duty=d)
        f.TriggerFactory.create(
            fixed_date=fix_to_date, fixed_assignment_state=Trigger.ASSIGNABLE,
            campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(0, result)
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [])

    def testSendable_CollectSendablesAssigned(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.TriggerFactory.create_batch(
            3, fixed_date=fix_to_date, fixed_assignment_state=Trigger.ASSIGNED,
            campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(0, result)
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [])


class TestTrigger(TestCase):
    def testTriggerFactory(self):
        t = f.TriggerFactory()
        self.assertTrue(Trigger.objects.filter(id=t.id).exists())

    def testGetFixedDateTriggersSetForADateAllAssignmentStates(self):
        fix_to_date = date(2005, 5, 5)
        triggers = f.TriggerFactory.create_batch(3, fixed_date=fix_to_date)
        f.TriggerFactory(fixed_date=date(2001, 1, 1))
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])

    def testGetFixedDateTriggersSetForADateAssignedWithNoAssigned(self):
        fix_to_date = date(2005, 5, 5)
        f.TriggerFactory.create_batch(
            3, fixed_date=fix_to_date, fixed_assignment_state=Trigger.ASSIGNED)
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [])

    def testGetFixedDateTriggersSetForADateAssignedWithAssigned(self):
        fix_to_date = date(2005, 5, 5)
        d = f.FullDutyFactory()
        c = f.CampaignFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        f.AssignmentFactory(volunteer=v, duty=d)
        triggers = f.TriggerFactory.create_batch(
            3, fixed_date=fix_to_date, fixed_assignment_state=Trigger.ASSIGNED,
            campaign=c)
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])

    # Skipped until I figure out how to use annotations for this.
    # def testGetFixedDateTriggersSetForADateAssignableWithAssigned(self):
    #     fix_to_date = date(2005, 5, 5)
    #     d = f.FullDutyFactory()
    #     c = f.CampaignFactory()
    #     c.events.add(d.event)
    #     v = f.VolunteerFactory()
    #     f.AssignmentFactory(volunteer=v, duty=d)
    #     f.TriggerFactory.create_batch(3, fixed_date=fix_to_date,
    #                                 fixed_assignment_state=Trigger.ASSIGNABLE,
    #                                 campaign=c)
    #     result = Trigger.objects.triggered(fix_to_date).order_by('id')
    #     self.assertQuerysetEqual(result, [])

    def testGetFixedDateTriggersSetForADateAssignableWithAssignable(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.AssignmentFactory(volunteer=v, duty=d)
        triggers = f.TriggerFactory.create_batch(
            3, fixed_date=fix_to_date,
            fixed_assignment_state=Trigger.ASSIGNABLE, campaign=c)
        result = Trigger.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])


class TestMessage(TestCase):
    def testMessageFactory(self):
        m = f.MessageFactory()
        self.assertTrue(Message.objects.filter(id=m.id).exists())

    def testRenderedBody(self):
        v = f.VolunteerFactory(dear_name="Joe")
        message = f.MessageFactory(body="Hi {{ volunteer.to_name }}")
        expected = "Hi Joe"
        result = message.rendered_body({'volunteer': v})
        self.assertEqual(expected, result)

    def testRenderedSubject(self):
        v = f.VolunteerFactory(dear_name="Joe")
        message = f.MessageFactory(subject="Go {{ volunteer.to_name }}")
        expected = "Go Joe"
        result = message.rendered_subject({'volunteer': v})
        self.assertEqual(expected, result)
