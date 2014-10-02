"""
Seed data in the database.
"""
from datetime import date

from django.core.management.base import BaseCommand

from volunteering import models


class Command(BaseCommand):
    help = 'Collect triggered messages and send any unsent ones'

    def handle(self, *args, **options):
        send_date = date.today()
        self.stdout.write("Collecting for %s" % send_date)

        collected = models.Sendable.collect_from_fixed_triggers(send_date)
        self.stdout.write("%s messages collected" % collected)

        collected = models.Sendable.collect_from_event_only_assigned_triggers(
            send_date)
        self.stdout.write("%s messages collected" % collected)
