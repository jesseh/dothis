# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0024_dutyeditable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField()),
                ('activities', models.ManyToManyField(to='volunteering.Activity', null=True, blank=True)),
                ('events', models.ManyToManyField(to='volunteering.Event', null=True, blank=True)),
                ('locations', models.ManyToManyField(to='volunteering.Location', null=True, blank=True)),
            ],
            options={
                'ordering': (b'-modified', b'-created'),
                'abstract': False,
                'get_latest_by': b'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fixed_date', models.DateField(help_text=b'Send the message on this specific day. If today or earlier the message will go immediately', null=True, blank=True)),
                ('fixed_assignment_state', models.IntegerField(default=2, choices=[(0, b'Assigned'), (1, b'Assignable'), (2, b'Assigned and assignable')])),
                ('event_based_days_before', models.PositiveIntegerField(help_text=b'Send the message this many days before the event.', null=True, blank=True)),
                ('event_based_assignment_state', models.IntegerField(default=2, choices=[(0, b'Assigned'), (1, b'Assignable'), (2, b'Assigned and assignable')])),
                ('assignment_based_days_after', models.PositiveIntegerField(help_text=b"Send the message this many days after the role was assigned the volunteer (including them assigning it themself). '0' will send the day they are assigned.", null=True, blank=True)),
                ('campaign', models.ForeignKey(blank=True, to='volunteering.Campaign', null=True)),
                ('message', models.ForeignKey(blank=True, to='volunteering.Message', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
