from django.test import TestCase

from volunteering.admin import make_event_copies, make_events_done
from volunteering.models import Event

import factories as f


class testEventActions(TestCase):

    def testMakeEventsDone(self):
        f.EventFactory.create_batch(2)
        qs = Event.objects.all()
        self.assertEqual(Event.objects.filter(is_done=True).count(), 0)
        make_events_done(None, None, qs)
        self.assertEqual(Event.objects.filter(is_done=True).count(), 2)

    def testCopyWithNothing(self):
        qs = Event.objects.none()
        make_event_copies(None, None, qs)
        self.assertTrue(True)

    def testCopyOne(self):
        f.EventFactory.create()
        qs = Event.objects.all()
        make_event_copies(None, None, qs)
        event_count = Event.objects.count()
        self.assertEqual(event_count, 2)

    def testCopyMultiple(self):
        f.EventFactory.create_batch(3)
        qs = Event.objects.all()
        make_event_copies(None, None, qs)
        event_count = Event.objects.count()
        self.assertEqual(event_count, 6)

    def testCopyingKeepsTheSameName(self):
        name_text = "orig name"
        f.EventFactory.create(name=name_text)
        qs = Event.objects.filter(name=name_text)
        make_event_copies(None, None, qs)
        self.assertEqual(Event.objects.filter(name=name_text).count(), 2)

    def testCopyingCarriesWebSummaryDescription(self):
        description_text = "some description"
        e = f.EventFactory.create(web_summary_description=description_text)
        qs = Event.objects.filter(id=e.id)
        make_event_copies(None, None, qs)
        self.assertEqual(
            Event.objects.filter(
                web_summary_description=description_text).count(), 2)

    def testCopyingCarriesAssignmentMessageDescription(self):
        description_text = "some description"
        e = f.EventFactory.create(
            assignment_message_description=description_text)
        qs = Event.objects.filter(id=e.id)
        make_event_copies(None, None, qs)
        self.assertEqual(
            Event.objects.filter(
                assignment_message_description=description_text).count(), 2)

    def testCopyingReplicatesDuties(self):
        e = f.EventFactory.create()
        f.FullDutyFactory.create(event=e)
        f.FullDutyFactory.create(event=e)
        qs = Event.objects.filter(id=e.id)
        make_event_copies(None, None, qs)
        for event in Event.objects.all():
            self.assertEqual(event.duty_set.count(), 2)
