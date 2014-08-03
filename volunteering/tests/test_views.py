from django.core.urlresolvers import reverse
from django.test import TestCase

from volunteering.models import (Activity, Assignment, Duty, Event, Location,
                                 Volunteer)


class testSummaryView(TestCase):
    def setUp(self):
        self.v = Volunteer.objects.create(name='Joe')
        self.e = Event.objects.create(
            name='an event', description='the short description')
        self.l = Location.objects.create(
            name='a location', description='the short description')
        self.a = Activity.objects.create(
            name='an activity', description='the short description')
        self.d = Duty.objects.create(event=self.e, location=self.l,
                                     activity=self.a)
        self.url = reverse('volunteering:summary',
                           kwargs={'volunteer_slug': self.v.slug})

    def testSummaryResponseCode(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def testSummaryContentIncludesActiveDuties(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.d.event.name)
        self.assertContains(response, self.d.location.name)
        self.assertContains(response, self.d.activity.name)

    def testSummaryContentOnlyShowsDutyOnce(self):
        self.d.multiple = 2
        self.d.save()
        response = self.client.get(self.url)
        self.assertContains(response, self.d.event.name, count=1)

    def testSummaryContentOnlyShowsDutyOnceIfAssigned(self):
        Assignment.objects.create(volunteer=self.v, duty=self.d)
        response = self.client.get(self.url)
        self.assertContains(response, self.d.event.name, count=1)
        self.assertContains(response, self.d.location.name, count=1)
        self.assertContains(response, self.d.activity.name, count=1)

    def testSummaryContentIncludesActivityName(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.d.activity.name)

    def testSummaryContentIncludesEventName(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.d.event.name)

    def testSummaryContentIncludesLocationName(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.d.location.name)


class testAssignmentView(TestCase):
    def setUp(self):
        self.v = Volunteer.objects.create(name='Joe')
        self.e = Event.objects.create(
            name='an event', description='the short description')
        self.l = Location.objects.create(
            name='a location', description='the short description')
        self.a = Activity.objects.create(
            name='an activity', description='the short description')
        self.d = Duty.objects.create(event=self.e, location=self.l,
                                     activity=self.a)
        self.url = reverse('volunteering:assignment',
                           kwargs={'volunteer_slug': self.v.slug,
                                   'duty_id': self.d.id})

    def testAssignmentGet(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def testGetContentIfAssigned(self):
        Assignment.objects.create(volunteer=self.v, duty=self.d)
        response = self.client.get(self.url)
        self.assertContains(response, "You have volunteered")
        self.assertContains(response, self.d.event.name, count=1)
        self.assertContains(response, self.d.location.name, count=1)
        self.assertContains(response, self.d.activity.name, count=1)

    def testGetContentIfUnassigned(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "have volunteered")
        self.assertContains(response, self.d.event.name, count=1)
        self.assertContains(response, self.d.location.name, count=1)
        self.assertContains(response, self.d.activity.name, count=1)

    def testAssignmentPost(self):
        self.assertFalse(
            Assignment.objects.filter(volunteer=self.v, duty=self.d).exists())
        response = self.client.post(self.url)
        self.assertTrue(
            Assignment.objects.filter(volunteer=self.v, duty=self.d).exists())
        self.assertRedirects(response, self.v.get_absolute_url())

    def testAssignmentPostWhenMultipleOfSameDuty(self):
        self.d.multiple = 2
        self.d.save()
        self.assertFalse(Assignment.objects.
                         filter(volunteer=self.v, duty=self.d).exists())
        response = self.client.post(self.url)
        self.assertTrue(Assignment.objects.
                        filter(volunteer=self.v, duty=self.d).exists())
        self.assertRedirects(response, self.v.get_absolute_url())

    def testNoPermissionToSeeAssignmentUnlessDutyIsAssignableOrAssigned(self):
        pass
