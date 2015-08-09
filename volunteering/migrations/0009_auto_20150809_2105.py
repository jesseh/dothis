# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0008_auto_20150809_2059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='triggerbyassignment',
            name='bcc',
        ),
        migrations.RemoveField(
            model_name='triggerbydate',
            name='bcc',
        ),
        migrations.RemoveField(
            model_name='triggerbyevent',
            name='bcc',
        ),
        migrations.AddField(
            model_name='campaign',
            name='bcc_address',
            field=models.EmailField(help_text=b'BCC selected campaign emails to this address.', max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='triggerbyassignment',
            name='send_to_bcc_address',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='triggerbydate',
            name='send_to_bcc_address',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='triggerbyevent',
            name='send_to_bcc_address',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
