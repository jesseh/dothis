# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0003_auto_20140803_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaignevent',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='campaignevent',
            name='event',
        ),
        migrations.AddField(
            model_name='campaign',
            name='activities',
            field=models.ManyToManyField(to=b'volunteering.Activity', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='events',
            field=models.ManyToManyField(to=b'volunteering.Event', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='locations',
            field=models.ManyToManyField(to=b'volunteering.Location', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='CampaignEvent',
        ),
    ]
