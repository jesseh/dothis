# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0042_auto_20140921_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriggerByEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days_before_event', models.PositiveIntegerField(help_text=b'Send the message this many days before the event.')),
                ('assignment_state', models.IntegerField(default=2, choices=[(0, b'With an assigned duty'), (1, b'Assignable to a duty'), (2, b'All recipients'), (3, b'No assigned duties')])),
                ('campaign', models.ForeignKey(blank=True, to='volunteering.Campaign', null=True)),
                ('message', models.ForeignKey(blank=True, to='volunteering.Message', null=True)),
            ],
            options={
                'ordering': ['campaign'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='trigger',
            name='event_based_assignment_state',
        ),
        migrations.RemoveField(
            model_name='trigger',
            name='event_based_days_before',
        ),
    ]
