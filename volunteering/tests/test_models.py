import unittest
from datetime import date, time

from django.db import IntegrityError
from django.test import TestCase

import factories as f

from volunteering.models import (Activity, Assignment, Attribute, Campaign,
                                 Duty, Event, Location, Sendable, TriggerBase,
                                 TriggerByDate, Message, Volunteer)


class TestAttribute(TestCase):
    def testHasAName(self):
        attribute = Attribute(name='yada')
        self.assertEqual('yada', attribute.name)

    def testAttributeIsUnique(self):
        f.AttributeFactory.create(name='yada')
        with self.assertRaises(Exception):
            f.AttributeFactory.create(name='yada')


class TestVolunteer(TestCase):
    def testVolunteerFactory(self):
        v = f.VolunteerFactory()
        self.assertTrue(Volunteer.objects.filter(id=v.id).exists())

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

    def testOneOnTodayIsAssignable(self):
        past_event = f.EventFactory(date=date(2111, 1, 1))
        f.DutyFactory.create(event=past_event)
        self.assertEqual(1, Duty.objects.assignable(
            as_of_date=date(2111, 1, 1)).count())

    def testOneInThePastIsNotAssignable(self):
        past_event = f.EventFactory(date=date(2000, 1, 1))
        f.DutyFactory.create(event=past_event)
        self.assertEqual(0, Duty.objects.assignable(
            as_of_date=date(2000, 1, 2)).count())

    def testOneOfOneIsAssignable(self):
        f.DutyFactory.create()
        self.assertEqual(1, Duty.objects.assignable().count())

    def testOneOfOneIsAssignableWhenMultiple2And1Assignment(self):
        duty = f.DutyFactory.create(multiple=2)
        f.AssignmentFactory(duty=duty)
        self.assertEqual(1, Duty.objects.assignable().count())

    def testNoneIsAssignableWhenMultiple2And2Assignments(self):
        duty = f.DutyFactory.create(multiple=2)
        f.AssignmentFactory(duty=duty)
        f.AssignmentFactory(duty=duty)
        self.assertEqual(0, Duty.objects.assignable().count())

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

    def testOneDutyIsAssignableToVolunteer_NoAttributes(self):
        f.DutyFactory.create()
        v = f.VolunteerFactory()
        self.assertEqual(1, Duty.objects.assignable_to(v).count())


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

    def testRecipientsWithInvalidArgs(self):
        campaign = f.CampaignFactory()
        with self.assertRaises(ValueError):
            campaign.recipients(True, False, True)
        with self.assertRaises(ValueError):
            campaign.recipients(False, True, True)
        with self.assertRaises(ValueError):
            campaign.recipients(True, True, True)

    def testRecipientsViaUnassigned(self):
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

        qs = campaign.recipients(unassigned=True).order_by('id')
        self.assertQuerysetEqual(qs, [repr(volunteer1)])

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

    def testPercentAssigned_NoDuties(self):
        campaign = f.CampaignFactory()
        self.assertEqual("0%", campaign.percent_assigned())

    def testPercentAssigned_IncreasinglyAssigned(self):
        duty1 = f.FullDutyFactory(multiple=2)
        duty2 = f.FullDutyFactory(multiple=2)
        campaign = f.CampaignFactory()
        campaign.events.add(duty1.event)
        campaign.events.add(duty2.event)
        volunteer1 = f.VolunteerFactory()
        volunteer2 = f.VolunteerFactory()
        self.assertEqual("0%", campaign.percent_assigned())
        f.AssignmentFactory(duty=duty1, volunteer=volunteer1)
        self.assertEqual("25%", campaign.percent_assigned())
        f.AssignmentFactory(duty=duty1, volunteer=volunteer2)
        self.assertEqual("50%", campaign.percent_assigned())
        f.AssignmentFactory(duty=duty2, volunteer=volunteer1)
        self.assertEqual("75%", campaign.percent_assigned())
        f.AssignmentFactory(duty=duty2, volunteer=volunteer2)
        self.assertEqual("100%", campaign.percent_assigned())

    def testVolunteersNeeded_NoDuties(self):
        campaign = f.CampaignFactory()
        self.assertEqual(0, campaign.volunteers_needed())

    def testVolunteersNeeded_OneDutyWithMultiple(self):
        campaign = f.CampaignFactory()
        duty = f.FullDutyFactory(multiple=5)
        campaign.events.add(duty.event)
        self.assertEqual(5, campaign.volunteers_needed())

    def testVolunteersNeeded_MultipleDutyWithMultiple(self):
        campaign = f.CampaignFactory()
        duty1 = f.FullDutyFactory(multiple=5)
        duty2 = f.FullDutyFactory(multiple=5)
        campaign.events.add(duty1.event)
        campaign.events.add(duty2.event)
        self.assertEqual(10, campaign.volunteers_needed())

    def testVolunteersAssigned_NoDuties(self):
        campaign = f.CampaignFactory()
        self.assertEqual(0, campaign.volunteers_assigned())

    def testVolunteersAssigned_OneDutyWithMultiple(self):
        campaign = f.CampaignFactory()
        duty = f.FullDutyFactory(multiple=5)
        f.AssignmentFactory(duty=duty)
        campaign.events.add(duty.event)
        self.assertEqual(1, campaign.volunteers_assigned())

    def testVolunteersAssigned_MultipleDutyWithMultiple(self):
        campaign = f.CampaignFactory()
        duty1 = f.FullDutyFactory(multiple=5)
        duty2 = f.FullDutyFactory(multiple=5)
        campaign.events.add(duty1.event)
        campaign.events.add(duty2.event)
        f.AssignmentFactory(duty=duty1)
        f.AssignmentFactory(duty=duty2)
        self.assertEqual(2, campaign.volunteers_assigned())


class TestAssignment(TestCase):

    def testHasTimestamps(self):
        assignment = f.AssignmentFactory()
        self.assertTrue(assignment.created)
        self.assertTrue(assignment.modified)

    def testNoDuplicates(self):
        a = f.AssignmentFactory.create()
        with self.assertRaises(IntegrityError):
            f.AssignmentFactory.create(volunteer=a.volunteer,
                                       duty=a.duty)

    @unittest.SkipTest
    def testHHServiceLocation(self):
        a = f.AssignmentFactory.create()
        self.assertEqual(a.hh_service_location(),
                         a.volunteer.family.hh_location_2014.name)


class TestActivity(TestCase):
    def setUp(self):
        self.a = f.ActivityFactory.build(
            name="the name",
            web_summary_description="the web summary description",
            assignment_message_description="assignment message description")

    def testHasAName(self):
        self.assertEqual(self.a.name, 'the name')

    def testNameIsUnique(self):
        self.a.save()
        with self.assertRaises(IntegrityError):
            Activity.objects.create(name='the name')

    def testHasAWebSummaryDescription(self):
        self.assertEqual(self.a.web_summary_description,
                         'the web summary description')

    def testHasAnAssignmentMessageDescription(self):
        self.assertEqual(self.a.assignment_message_description,
                         'assignment message description')


class TestEvent(TestCase):
    def setUp(self):
        self.a = Event(
            name="the name",
            web_summary_description="the web summary description",
            assignment_message_description="assignment message description",
            date=date(2001, 1, 1))

    def testHasAName(self):
        self.assertEqual(self.a.name, 'the name')

    def testHasAWebSummaryDescription(self):
        self.assertEqual(self.a.web_summary_description,
                         'the web summary description')

    def testHasAnAssignmentMessageDescription(self):
        self.assertEqual(self.a.assignment_message_description,
                         'assignment message description')

    def testHasADate(self):
        self.assertEqual(self.a.date, date(2001, 1, 1))

    def testDefaultsToNotDone(self):
        self.assertTrue(self.a.is_active)


class TestLocation(TestCase):
    def setUp(self):
        self.l = Location(
            name="the name",
            web_summary_description="the web summary description",
            assignment_message_description="assignment message description")

    def testHasAName(self):
        self.assertEqual(self.l.name, 'the name')

    def testNameIsUnique(self):
        self.l.save()
        with self.assertRaises(IntegrityError):
            Location.objects.create(name='the name')

    def testHasAWebSummaryDescription(self):
        self.assertEqual(self.l.web_summary_description,
                         'the web summary description')

    def testHasAnAssignmentMessageDescription(self):
        self.assertEqual(self.l.assignment_message_description,
                         'assignment message description')


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

    def testSendable_DateCollectSendablesAssignable(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.TriggerByDateFactory.create_batch(
            3, fixed_date=fix_to_date,
            assignment_state=TriggerBase.ASSIGNABLE, campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(3, result)
        all_qs = Sendable.objects.all().order_by('id')
        self.assertQuerysetEqual(all_qs, [v, v, v],
                                 transform=lambda s: s.volunteer)

    def testSendable_DateCollectSendablesAssignableButAlreadyAssigned(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.AssignmentFactory(volunteer=v, duty=d)
        f.TriggerByDateFactory.create(
            fixed_date=fix_to_date,
            assignment_state=TriggerBase.ASSIGNABLE,
            campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(0, result)
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [])

    def testSendable_DateCollectSndblesUnassignedButAssignedOnce(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d, d2 = f.FullDutyFactory.create_batch(2)
        c.events.add(d.event)
        c.events.add(d2.event)
        v, v2, _ = f.VolunteerFactory.create_batch(3)
        a = f.AttributeFactory()
        v.attributes.add(a)
        v2.attributes.add(a)
        d.activity.attributes.add(a)
        d2.activity.attributes.add(a)

        f.AssignmentFactory(volunteer=v, duty=d)
        f.TriggerByDateFactory.create(
            fixed_date=fix_to_date,
            assignment_state=TriggerBase.UNASSIGNED,
            campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(1, result)
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [v2],
                                 transform=lambda s: s.volunteer)

    def testSendable_DateCollectSendablesAssigned(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.TriggerByDateFactory.create_batch(
            3, fixed_date=fix_to_date,
            assignment_state=TriggerBase.ASSIGNED,
            campaign=c)
        result = Sendable.collect_from_fixed_triggers(fix_to_date)
        self.assertEqual(0, result)
        all_qs = Sendable.objects.all()
        self.assertQuerysetEqual(all_qs, [])

    def testSendable_EventCollectSendablesAssignable(self):
        fix_to_date = date(2225, 5, 5)  # This must be in the future.
        e = f.EventFactory(date=fix_to_date)
        c = f.CampaignFactory()
        d = f.FullDutyFactory(event=e)
        c.events.add(e)
        v = f.VolunteerFactory()
        f.AssignmentFactory(volunteer=v, duty=d)
        f.TriggerByEventFactory.create_batch(
            3, assignment_state=TriggerBase.ASSIGNED, campaign=c)
        result = Sendable.collect_from_event_only_assigned_triggers(
            fix_to_date)
        self.assertEqual(3, result)
        all_qs = Sendable.objects.all().order_by('id')
        self.assertQuerysetEqual(all_qs, [v, v, v],
                                 transform=lambda s: s.volunteer)

#     def testSendable_EventCollectSendablesAssignableButAlreadyAssigned(self):
#         fix_to_date = date(2005, 5, 5)
#         c = f.CampaignFactory()
#         d = f.FullDutyFactory()
#         c.events.add(d.event)
#         v = f.VolunteerFactory()
#         a = f.AttributeFactory()
#         v.attributes.add(a)
#         d.activity.attributes.add(a)
#         f.AssignmentFactory(volunteer=v, duty=d)
#         f.TriggerByEventFactory.create(
#             fixed_date=fix_to_date,
#             assignment_state=TriggerBase.ASSIGNABLE,
#             campaign=c)
#         result = Sendable.collect_from_fixed_triggers(fix_to_date)
#         self.assertEqual(0, result)
#         all_qs = Sendable.objects.all()
#         self.assertQuerysetEqual(all_qs, [])

#     def testSendable_EventCollectSndblsUnassignedButAssignedOnce(self):
#         fix_to_date = date(2005, 5, 5)
#         c = f.CampaignFactory()
#         d, d2 = f.FullDutyFactory.create_batch(2)
#         c.events.add(d.event)
#         c.events.add(d2.event)
#         v, v2, _ = f.VolunteerFactory.create_batch(3)
#         a = f.AttributeFactory()
#         v.attributes.add(a)
#         v2.attributes.add(a)
#         d.activity.attributes.add(a)
#         d2.activity.attributes.add(a)

#         f.AssignmentFactory(volunteer=v, duty=d)
#         f.TriggerByEventFactory.create(
#             fixed_date=fix_to_date,
#             assignment_state=TriggerBase.UNASSIGNED,
#             campaign=c)
#         result = Sendable.collect_from_fixed_triggers(fix_to_date)
#         self.assertEqual(1, result)
#         all_qs = Sendable.objects.all()
#         self.assertQuerysetEqual(all_qs, [v2],
#                                  transform=lambda s: s.volunteer)

#     def testSendable_EventCollectSendablesAssigned(self):
#         fix_to_date = date(2005, 5, 5)
#         c = f.CampaignFactory()
#         d = f.FullDutyFactory()
#         c.events.add(d.event)
#         v = f.VolunteerFactory()
#         a = f.AttributeFactory()
#         v.attributes.add(a)
#         d.activity.attributes.add(a)
#         f.TriggerByEventFactory.create_batch(
#             3, fixed_date=fix_to_date,
#             assignment_state=TriggerBase.ASSIGNED,
#             campaign=c)
#         result = Sendable.collect_from_fixed_triggers(fix_to_date)
#         self.assertEqual(0, result)
#         all_qs = Sendable.objects.all()
#         self.assertQuerysetEqual(all_qs, [])


class TestTriggerByDate(TestCase):
    def testTriggerByDateFactory(self):
        t = f.TriggerByDateFactory()
        self.assertTrue(TriggerByDate.objects.filter(id=t.id).exists())

    def testGetSetForADateAllAssignmentStates(self):
        fix_to_date = date(2005, 5, 5)
        triggers = f.TriggerByDateFactory.create_batch(3,
                                                       fixed_date=fix_to_date)
        f.TriggerByDateFactory(fixed_date=date(2001, 1, 1))
        result = TriggerByDate.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])

    def testGetSetForADateAssignedWithNoAssigned(self):
        fix_to_date = date(2005, 5, 5)
        f.TriggerByDateFactory.create_batch(
            3, fixed_date=fix_to_date,
            assignment_state=TriggerBase.ASSIGNED)
        result = TriggerByDate.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [])

    def testGetSetForADateAssignedWithAssigned(self):
        fix_to_date = date(2005, 5, 5)
        d = f.FullDutyFactory()
        c = f.CampaignFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        f.AssignmentFactory(volunteer=v, duty=d)
        triggers = f.TriggerByDateFactory.create_batch(
            3, fixed_date=fix_to_date,
            assignment_state=TriggerBase.ASSIGNED,
            campaign=c)
        result = TriggerByDate.objects.triggered(fix_to_date).order_by('id')
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
    #                                 assignment_state=Trigger.ASSIGNABLE,
    #                                 campaign=c)
    #     result = Trigger.objects.triggered(fix_to_date).order_by('id')
    #     self.assertQuerysetEqual(result, [])

    def testGetSetForADateAssignableWithAssignable(self):
        fix_to_date = date(2005, 5, 5)
        c = f.CampaignFactory()
        d = f.FullDutyFactory()
        c.events.add(d.event)
        v = f.VolunteerFactory()
        a = f.AttributeFactory()
        v.attributes.add(a)
        d.activity.attributes.add(a)
        f.AssignmentFactory(volunteer=v, duty=d)
        triggers = f.TriggerByDateFactory.create_batch(
            3, fixed_date=fix_to_date,
            assignment_state=TriggerBase.ASSIGNABLE, campaign=c)
        result = TriggerByDate.objects.triggered(fix_to_date).order_by('id')
        self.assertQuerysetEqual(result, [repr(t) for t in triggers])


class TestMessage(TestCase):
    def testMessageFactory(self):
        m = f.MessageFactory()
        self.assertTrue(Message.objects.filter(id=m.id).exists())

    def testSMSFactory(self):
        m = f.MessageSMSFactory()
        self.assertTrue(Message.objects.filter(id=m.id).exists())
        self.assertEqual('sms', m.get_mode_display())

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
