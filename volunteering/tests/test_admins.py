from django.test import TestCase

from volunteering.admin import make_event_copies
from volunteering.models import Event

import factories as f


class testMakeEventCopies(TestCase):

    def testCopyWithNothing(self):
        qs = Event.objects.none()
        make_event_copies(None, None, qs)
        self.assertTrue(True)

    def testCopyOne(self):
        f.EventFactory.create()
        qs = Event.objects.all()
        make_event_copies(None, None, qs)
        event_count = Event.objects.count()
        self.assertEquals(event_count, 2)

    def testCopyingPrependsToTheName(self):
        name_text = "orig name"
        f.EventFactory.create(name=name_text)
        qs = Event.objects.filter(name=name_text)
        make_event_copies(None, None, qs)
        self.assertTrue(Event.objects.get(name="copy of " + name_text))

    def testCopyingCarriesWebSummaryDescription(self):
        description_text = "some description"
        e = f.EventFactory.create(web_summary_description=description_text)
        qs = Event.objects.filter(id=e.id)
        make_event_copies(None, None, qs)
        self.assertEquals(
            Event.objects.filter(
                web_summary_description=description_text).count(), 2)

    def testCopyingCarriesAssignmentMessageDescription(self):
        description_text = "some description"
        e = f.EventFactory.create(
            assignment_message_description=description_text)
        qs = Event.objects.filter(id=e.id)
        make_event_copies(None, None, qs)
        self.assertEquals(
            Event.objects.filter(
                assignment_message_description=description_text).count(), 2)
