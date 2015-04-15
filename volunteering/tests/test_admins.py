from django.test import TestCase

from volunteering.admin import (copy_events, activate_events,
                                deactivate_events, archive_events,
                                unarchive_events)
from volunteering.models import Event

import factories as f


class testEventActions(TestCase):

    def testMakeEventsActive(self):
        f.EventFactory.create_batch(2, is_active=False)
        qs = Event.objects.all()
        self.assertEqual(Event.objects.filter(is_active=False).count(), 2)
        activate_events(None, None, qs)
        self.assertEqual(Event.objects.filter(is_active=False).count(), 0)

    def testMakeEventsNotActive(self):
        f.EventFactory.create_batch(2)
        qs = Event.objects.all()
        self.assertEqual(Event.objects.filter(is_active=False).count(), 0)
        deactivate_events(None, None, qs)
        self.assertEqual(Event.objects.filter(is_active=False).count(), 2)

    def testMakeEventsArchived(self):
        f.EventFactory.create_batch(2, is_archived=False)
        qs = Event.objects.all()
        self.assertEqual(Event.objects.filter(is_archived=False).count(), 2)
        archive_events(None, None, qs)
        self.assertEqual(Event.objects.filter(is_archived=False).count(), 0)

    def testMakeEventsUnarchived(self):
        f.EventFactory.create_batch(2, is_archived=True)
        qs = Event.objects.all()
        self.assertEqual(Event.objects.filter(is_archived=False).count(), 0)
        unarchive_events(None, None, qs)
        self.assertEqual(Event.objects.filter(is_archived=False).count(), 2)

    def testCopyWithNothing(self):
        qs = Event.objects.none()
        copy_events(None, None, qs)
        self.assertTrue(True)

    def testCopyOne(self):
        f.EventFactory.create()
        qs = Event.objects.all()
        copy_events(None, None, qs)
        event_count = Event.objects.count()
        self.assertEqual(event_count, 2)

    def testCopyMultiple(self):
        f.EventFactory.create_batch(3)
        qs = Event.objects.all()
        copy_events(None, None, qs)
        event_count = Event.objects.count()
        self.assertEqual(event_count, 6)

    def testCopyingKeepsTheSameName(self):
        name_text = "orig name"
        f.EventFactory.create(name=name_text)
        qs = Event.objects.filter(name=name_text)
        copy_events(None, None, qs)
        self.assertEqual(Event.objects.filter(name=name_text).count(), 2)

    def testCopyingCarriesWebSummaryDescription(self):
        description_text = "some description"
        e = f.EventFactory.create(web_summary_description=description_text)
        qs = Event.objects.filter(id=e.id)
        copy_events(None, None, qs)
        self.assertEqual(
            Event.objects.filter(
                web_summary_description=description_text).count(), 2)

    def testCopyingCarriesAssignmentMessageDescription(self):
        description_text = "some description"
        e = f.EventFactory.create(
            assignment_message_description=description_text)
        qs = Event.objects.filter(id=e.id)
        copy_events(None, None, qs)
        self.assertEqual(
            Event.objects.filter(
                assignment_message_description=description_text).count(), 2)

    def testCopyingReplicatesDuties(self):
        e = f.EventFactory.create()
        f.FullDutyFactory.create(event=e)
        f.FullDutyFactory.create(event=e)
        qs = Event.objects.filter(id=e.id)
        copy_events(None, None, qs)
        for event in Event.objects.all():
            self.assertEqual(event.duty_set.count(), 2)
