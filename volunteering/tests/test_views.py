from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from volunteering.models import (Activity, Assignment, Campaign, CampaignDuty,
                                 Duty, Event, Location, Volunteer)


class testSummaryView(TestCase):
    def setUp(self):
        self.v = Volunteer.objects.create(name='Joe')
        self.c = Campaign.objects.create(name='a campaign', slug='c_slug')
        self.e = Event.objects.create(
            name='an event', short_description='the short description')
        self.l = Location.objects.create(
            name='a location', short_description='the short description')
        self.a = Activity.objects.create(
            name='an activity', short_description='the short description')
        self.d = Duty.objects.create(event=self.e, location=self.l,
                                     activity=self.a)
        self.cd = CampaignDuty.objects.create(campaign=self.c,
                                              duty=self.d)
        self.url = reverse('volunteering:summary',
                           kwargs={'volunteer_slug': self.v.slug})

    def testSummaryResponseCode(self):
        response = Client().get(self.url)
        self.assertEqual(200, response.status_code)

    def testSummaryContentIncludesActiveCampaigns(self):
        response = Client().get(self.url)
        self.assertContains(response, self.c.name)

    def testSummaryContentExcludesInactiveCampaigns(self):
        self.c.deactivate()
        self.c.save()
        response = Client().get(self.url)
        self.assertNotContains(response, self.c.name)

    def testSummaryContentOnlyShowsCampaignDutyOnce(self):
        CampaignDuty.objects.create(campaign=self.c, duty=self.d)
        response = Client().get(self.url)
        self.assertContains(response, self.c.name, count=1)

    def testSummaryContentOnlyShowsCampaignDutyOnceIfAssigned(self):
        CampaignDuty.objects.create(campaign=self.c, duty=self.d)
        Assignment.objects.create(volunteer=self.v, campaign_duty=self.cd)
        response = Client().get(self.url)
        self.assertContains(response, self.c.name, count=1)

    def testSummaryContentIncludesActivityShortDescription(self):
        response = Client().get(self.url)
        self.assertContains(response, self.c.name)


class testAssignmentView(TestCase):
    def setUp(self):
        self.v, _ = Volunteer.objects.get_or_create(name='Joe')
        self.c, _ = Campaign.objects.get_or_create(name='a campaign',
                                                   slug='c_slug')
        self.e = Event.objects.create(
            name='an event', short_description='the short description')
        self.l = Location.objects.create(
            name='a location', short_description='the short description')
        self.a = Activity.objects.create(
            name='an activity', short_description='the short description')
        self.d = Duty.objects.create(event=self.e, location=self.l,
                                     activity=self.a)
        self.cd, _ = CampaignDuty.objects.get_or_create(campaign=self.c,
                                                        duty=self.d)
        self.url = reverse('volunteering:assignment',
                           kwargs={'volunteer_slug': self.v.slug,
                                   'campaign_slug': self.c.slug,
                                   'duty_id': self.d.id})

    def testAssignmentGet(self):
        response = Client().get(self.url)
        self.assertEqual(200, response.status_code)

    def testAssignmentPost(self):
        self.assertFalse(
            Assignment.objects.filter(volunteer=self.v,
                                      campaign_duty=self.cd).exists())
        response = Client().post(self.url)
        self.assertTrue(
            Assignment.objects.filter(volunteer=self.v,
                                      campaign_duty=self.cd).exists())
        self.assertRedirects(response, self.v.get_absolute_url())

    def testAssignmentPostWhenMultipleOfSameCampaignDuty(self):
        cd2 = CampaignDuty.objects.create(campaign=self.c, duty=self.d)
        self.assertFalse(
            Assignment.objects.filter(volunteer=self.v,
                                      campaign_duty=cd2).exists())
        response = Client().post(self.url)
        self.assertTrue(
            Assignment.objects.filter(volunteer=self.v,
                                      campaign_duty=cd2).exists())
        self.assertRedirects(response, self.v.get_absolute_url())
