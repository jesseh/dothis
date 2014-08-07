# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0030_sendable_send_failed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sendable',
            options={},
        ),
        migrations.AlterField(
            model_name='duty',
            name='assignments',
            field=models.ManyToManyField(to=b'volunteering.Volunteer', through='volunteering.Assignment', db_index=True),
        ),
        migrations.AlterField(
            model_name='trigger',
            name='fixed_date',
            field=models.DateField(help_text=b'Send the message on this specific day. If today or earlier the message will go immediately', null=True, db_index=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='sendable',
            unique_together=set([(b'send_date', b'trigger', b'volunteer', b'assignment')]),
        ),
    ]
