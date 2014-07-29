from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from volunteering.models import (Assignment, Campaign, CampaignDuty, Duty,
                                 Volunteer)


class testSummaryView(TestCase):
    def setUp(self):
        self.v, _ = Volunteer.objects.get_or_create(name='Joe')
        self.c, _ = Campaign.objects.get_or_create(name='a campaign',
                                                   slug='c_slug')
        self.d, _ = Duty.objects.get_or_create(name='a duty', slug='d_slug')
        self.cd, _ = CampaignDuty.objects.get_or_create(campaign=self.c,
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


class testAssignmentView(TestCase):
    def setUp(self):
        self.v, _ = Volunteer.objects.get_or_create(name='Joe')
        self.c, _ = Campaign.objects.get_or_create(name='a campaign',
                                                   slug='c_slug')
        self.d, _ = Duty.objects.get_or_create(name='a duty', slug='d_slug')
        self.cd, _ = CampaignDuty.objects.get_or_create(campaign=self.c,
                                                        duty=self.d)
        self.url = reverse('volunteering:assignment',
                           kwargs={'volunteer_slug': self.v.slug,
                                   'campaign_slug': self.c.slug,
                                   'duty_slug': self.d.slug})

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
