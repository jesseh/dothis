# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0041_auto_20140912_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='TriggerByAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days_after', models.PositiveIntegerField(help_text=b"Send the message this many days after the role was assigned to the volunteer (including them assigning it themself). '0' will send the day they are assigned.")),
                ('campaign', models.ForeignKey(blank=True, to='volunteering.Campaign', null=True)),
                ('message', models.ForeignKey(blank=True, to='volunteering.Message', null=True)),
            ],
            options={
                'ordering': [b'campaign'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='campaign',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='sendable',
            options={},
        ),
        migrations.RemoveField(
            model_name='trigger',
            name='assignment_based_days_after',
        ),
    ]
