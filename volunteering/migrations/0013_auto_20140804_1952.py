# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0012_duty_coordinator_note'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='duty',
            unique_together=set([(b'activity', b'event', b'location', b'start_time', b'end_time')]),
        ),
    ]
