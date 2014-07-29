import unittest

from django.db import IntegrityError

from volunteering.models import (Assignment, Attribute, Campaign, CampaignDuty,
                                 Duty, Volunteer)


class TestAttribute(unittest.TestCase):
    def testHasAName(self):
        attribute = Attribute(name='yada')
        self.assertEqual('yada', attribute.name)

    def testAttributeIsUnique(self):
        Attribute(name='yada').save()
        with self.assertRaises(Exception):
            Attribute(name='yada').save()


class TestVolunteer(unittest.TestCase):
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
        campaign = Campaign.objects.create(slug="a campaign")
        duty = Duty.objects.create(name="A duty")
        self.assertFalse(volunteer.has_claimed(campaign, duty))

    def testHasClaimed_IsTrueWhenTrue(self):
        volunteer = Volunteer.objects.create(name='tester')
        campaign = Campaign.objects.create(slug="a campaign")
        duty = Duty.objects.create(name="A duty")
        c_duty = CampaignDuty.objects.create(campaign=campaign, duty=duty)
        Assignment.objects.create(volunteer=volunteer, campaign_duty=c_duty)
        self.assertTrue(volunteer.has_claimed(campaign, duty))


class TestDuty(unittest.TestCase):
    def testSettingAnAttribute(self):
        d = Duty.objects.create(name='a duty')
        d.attributes.create(name='attr')
        self.assertEqual('attr', d.attributes.all()[0].name)

    def testHasSlug(self):
        d = Duty(slug='a slug')
        self.assertEqual('a slug', d.slug)


class TestCampaign(unittest.TestCase):
    def testHasSlug(self):
        c = Campaign(slug='a slug')
        self.assertEqual('a slug', c.slug)

    def testIsActiveInitially(self):
        c = Campaign(slug='a slug')
        self.assertEqual(1, c.status)

    def testDeactivate(self):
        c = Campaign(slug='a slug')
        c.deactivate()
        self.assertEqual(0, c.status)


class TestCampaignDuty(unittest.TestCase):
    def setUp(self):
        self.campaign = Campaign(name="a campaign", slug="a_campaign")
        self.duty = Duty(name="a duty", slug="a_duty")

    def testHasTimestamps(self):
        c = CampaignDuty(duty=self.duty, campaign=self.campaign)
        self.assertTrue(c.created)
        self.assertTrue(c.modified)


class TestAssignment(unittest.TestCase):

    def setUp(self):
        self.campaign = Campaign.objects.create(name="a campaign",
                                                slug="a_campaign")
        self.duty = Duty.objects.create(name="a duty", slug="a_duty")
        self.c_duty = CampaignDuty.objects.create(duty=self.duty,
                                                  campaign=self.campaign)
        self.volunteer = Volunteer.objects.create(name='tester')

    def testHasTimestamps(self):
        assignment = Assignment(volunteer=self.volunteer,
                                campaign_duty=self.c_duty)
        self.assertTrue(assignment.created)
        self.assertTrue(assignment.modified)

    def testNoDuplicates(self):
        Assignment.objects.create(volunteer=self.volunteer,
                                  campaign_duty=self.c_duty)
        with self.assertRaises(IntegrityError):
            Assignment.objects.create(volunteer=self.volunteer,
                                      campaign_duty=self.c_duty)
