"""
Seed data in the database.
"""
from django.core.management.base import BaseCommand

from volunteering import models


class Command(BaseCommand):
    help = 'Send any unsent ones'

    def handle(self, *args, **options):
        sent = models.Sendable.send_unsent()
        self.stdout.write("%s messages sent" % sent)
