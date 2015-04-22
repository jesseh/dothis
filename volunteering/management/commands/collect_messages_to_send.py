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
        self.stdout.write("Collecting for %s\n" % send_date)
        models.Sendable.collect_all(send_date, self.stdout, verbose=True)
