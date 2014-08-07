# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0025_campaign_message_trigger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sendable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('send_date', models.DateField(null=True, blank=True)),
                ('assignment', models.ForeignKey(to='volunteering.Assignment')),
                ('trigger', models.ForeignKey(to='volunteering.Trigger')),
                ('volunteer', models.ForeignKey(to='volunteering.Volunteer')),
            ],
            options={
                'ordering': (b'-modified', b'-created'),
                'abstract': False,
                'get_latest_by': b'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='trigger',
            name='assignment_based_days_after',
            field=models.PositiveIntegerField(help_text=b"Send the message this many days after the role was assigned to the volunteer (including them assigning it themself). '0' will send the day they are assigned.", null=True, blank=True),
        ),
    ]
