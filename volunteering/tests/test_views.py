from django.core.urlresolvers import reverse
from django.test import TestCase

import factories as f

from volunteering.models import (Assignment, Volunteer)


class testSummaryView(TestCase):
    def setUp(self):
        self.v = f.VolunteerFactory.create()
        self.e = f.EventFactory()
        self.l = f.LocationFactory()
        self.a = f.ActivityFactory()
        self.d = f.DutyFactory.create(
            event=self.e, location=self.l, activity=self.a)
        self.url = reverse('volunteering:summary',
                           kwargs={'volunteer_slug': self.v.slug})

    def testSummaryResponseCode(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def testSummaryViewSetsLastSummaryViewDate(self):
        self.assertIsNone(self.v.last_summary_view)
        self.client.get(self.url)
        d1 = Volunteer.objects.get(id=self.v.id).last_summary_view
        self.assertIsNotNone(d1)
        self.client.get(self.url)
        d2 = Volunteer.objects.get(id=self.v.id).last_summary_view
        self.assertTrue(d1 < d2)

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
        f.AssignmentFactory.create(volunteer=self.v, duty=self.d)
        response = self.client.get(self.url)
        self.assertContains(response, self.d.event.name, count=1)
        self.assertContains(response, self.d.location.name, count=1)
        self.assertContains(response, self.d.activity.name, count=1)

    def testSummaryContentIncludesVolunteerInitials(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.v.initials())

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
        self.v = f.VolunteerFactory.create()
        self.e = f.EventFactory.create()
        self.l = f.LocationFactory.create()
        self.a = f.ActivityFactory.create()
        self.d = f.DutyFactory.create(event=self.e, location=self.l,
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
        self.assertContains(response, "Thanks")
        self.assertContains(response, self.v.initials())
        self.assertContains(response, self.d.event.name, count=1)
        self.assertContains(response, self.d.location.name, count=1)
        self.assertContains(response, self.d.activity.name, count=1)

    def testGetContentIfUnassigned(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "Thanks")
        self.assertContains(response, self.d.event.name, count=1)
        self.assertContains(response, self.d.location.name, count=1)
        self.assertContains(response, self.d.activity.name, count=1)

    def testAssignmentPost(self):
        self.assertFalse(
            Assignment.objects.filter(volunteer=self.v, duty=self.d).exists())
        response = self.client.post(self.url)
        self.assertTrue(
            Assignment.objects.filter(volunteer=self.v, duty=self.d).exists())
        self.assertRedirects(response, self.url)

    def testAssignmentPostWhenMultipleOfSameDuty(self):
        self.d.multiple = 2
        self.d.save()
        self.assertFalse(Assignment.objects.
                         filter(volunteer=self.v, duty=self.d).exists())
        response = self.client.post(self.url)
        self.assertTrue(Assignment.objects.
                        filter(volunteer=self.v, duty=self.d).exists())
        self.assertRedirects(response, self.url)

    def testNoPermissionToSeeAssignmentUnlessDutyIsAssignableOrAssigned(self):
        pass
