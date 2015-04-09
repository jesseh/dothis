# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    replaces = [
        (b'volunteering', '0001_initial'),
        (b'volunteering', '0002_auto_20140731_1749'),
        (b'volunteering', '0003_auto_20140803_1123'),
        (b'volunteering', '0004_auto_20140803_1701'),
        (b'volunteering', '0005_auto_20140803_1708'),
        (b'volunteering', '0006_campaign_assignment_state'),
        (b'volunteering', '0007_campaign_start_date'),
        (b'volunteering', '0008_remove_campaign_start_date'),
        (b'volunteering', '0009_auto_20140803_1757'),
        (b'volunteering', '0010_auto_20140803_1808'),
        (b'volunteering', '0011_duty_details'),
        (b'volunteering', '0012_duty_coordinator_note'),
        (b'volunteering', '0013_auto_20140804_1952'),
        (b'volunteering', '0014_auto_20140805_0018'),
        (b'volunteering', '0015_auto_20140805_0219'),
        (b'volunteering', '0016_auto_20140805_0305'),
        (b'volunteering', '0017_auto_20140805_0316'),
        (b'volunteering', '0018_auto_20140805_1239'),
        (b'volunteering', '0019_auto_20140805_1240'),
        (b'volunteering', '0020_auto_20140805_1243'),
        (b'volunteering', '0021_auto_20140805_1604'),
        (b'volunteering', '0022_auto_20140805_2113'),
        (b'volunteering', '0023_auto_20140806_1432'),
        (b'volunteering', '0024_dutyeditable'),
        (b'volunteering', '0025_campaign_message_trigger'),
        (b'volunteering', '0026_auto_20140806_1740'),
        (b'volunteering', '0027_auto_20140806_1906'),
        (b'volunteering', '0028_auto_20140807_0801'),
        (b'volunteering', '0029_message_body_is_html'),
        (b'volunteering', '0030_sendable_send_failed'),
        (b'volunteering', '0031_auto_20140807_2026'),
        (b'volunteering', '0032_auto_20140807_2138'),
        (b'volunteering', '0033_auto_20140807_2140'),
        (b'volunteering', '0034_auto_20140808_2125'),
        (b'volunteering', '0035_auto_20140808_2141'),
        (b'volunteering', '0036_auto_20140810_1255'),
        (b'volunteering', '0037_auto_20140811_1654'),
        (b'volunteering', '0038_auto_20140828_1334'),
        (b'volunteering', '0039_auto_20140901_2002'),
        (b'volunteering', '0040_auto_20140912_0802'),
        (b'volunteering', '0041_auto_20140912_0805'),
        (b'volunteering', '0042_auto_20140921_0852'),
        (b'volunteering', '0043_auto_20140921_0907'),
        (b'volunteering', '0044_auto_20140921_0908'),
        (b'volunteering', '0045_auto_20140921_1249'),
        (b'volunteering', '0046_auto_20140921_1258'),
        (b'volunteering', '0047_auto_20140921_1301'),
        (b'volunteering', '0048_remove_sendable_orig_trigger'),
        (b'volunteering', '0049_auto_20140921_1748'),
        (b'volunteering', '0050_auto_20140921_1940'),
        (b'volunteering', '0051_message_mode'),
        (b'volunteering', '0052_auto_20141006_1954'),
        (b'volunteering', '0053_auto_20141219_1044'),
        (b'volunteering', '0054_auto_20141219_1058'),
        (b'volunteering', '0055_auto_20150125_0251'),
        (b'volunteering', '0056_event_is_past'),
        (b'volunteering', '0057_auto_20150126_2232'),
        (b'volunteering', '0058_auto_20150126_2346'),
        (b'volunteering', '0059_auto_20150409_1457')
        ]

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('web_summary_description', models.TextField(default=b'', blank=True)),
                ('assignment_message_description', models.TextField(default=b'', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField()),
                ('activities', models.ManyToManyField(to='volunteering.Activity', null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField(null=True, blank=True)),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('multiple', models.PositiveIntegerField(default=1, help_text=b'The number of volunteers needed for this duty.')),
                ('details', models.TextField(blank=True)),
                ('coordinator_note', models.TextField(blank=True)),
                ('activity', models.ForeignKey(blank=True, to='volunteering.Activity', null=True)),
            ],
            options={
                'ordering': ['event', 'start_time', 'activity', 'location'],
                'verbose_name_plural': 'Duties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField(null=True, blank=True)),
                ('web_summary_description', models.TextField(default=b'', blank=True)),
                ('assignment_message_description', models.TextField(default=b'', blank=True)),
                ('is_active', models.BooleanField(default=True, db_index=True)),
            ],
            options={
                'ordering': ['date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.CharField(unique=True, max_length=200)),
                ('hh_location_2014', models.IntegerField(blank=True, null=True, choices=[(1, b'Regent Suite'), (2, b'Shul')])),
            ],
            options={
                'ordering': ['external_id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('web_summary_description', models.TextField(default=b'', blank=True)),
                ('assignment_message_description', models.TextField(default=b'', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('mode', models.IntegerField(default=0, choices=[(0, b'email'), (1, b'sms')])),
                ('subject', models.CharField(help_text=b'not used for SMS', max_length=200)),
                ('body', models.TextField(blank=True)),
                ('body_is_html', models.BooleanField(default=False, help_text=b'not used for SMS')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sendable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('send_date', models.DateField(db_index=True)),
                ('sent_date', models.DateField(db_index=True, null=True, blank=True)),
                ('send_failed', models.BooleanField(default=False, db_index=True)),
                ('trigger_id', models.PositiveIntegerField()),
                ('assignment', models.ForeignKey(blank=True, to='volunteering.Assignment', null=True)),
                ('trigger_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TriggerByAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days_after', models.PositiveIntegerField(help_text=b"Send the message this many days after the role was assigned to the volunteer (including them assigning it themself). '0' will send the day they are assigned.")),
                ('campaign', models.ForeignKey(blank=True, to='volunteering.Campaign', null=True)),
                ('message', models.ForeignKey(blank=True, to='volunteering.Message', null=True)),
            ],
            options={
                'ordering': ['campaign'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TriggerByDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fixed_date', models.DateField(help_text=b'Send the message on this specific day. If today or earlier the message will go immediately', null=True, db_index=True, blank=True)),
                ('assignment_state', models.IntegerField(default=2, choices=[(0, b'With an assigned duty'), (1, b'Assignable to a duty'), (2, b'All recipients'), (3, b'No assigned duties')])),
                ('campaign', models.ForeignKey(blank=True, to='volunteering.Campaign', null=True)),
                ('message', models.ForeignKey(blank=True, to='volunteering.Message', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TriggerByEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days_before', models.PositiveIntegerField(help_text=b'Send the message this many days before the event.')),
                ('assignment_state', models.IntegerField(default=0, choices=[(0, b'With an assigned duty')])),
                ('campaign', models.ForeignKey(blank=True, to='volunteering.Campaign', null=True)),
                ('message', models.ForeignKey(blank=True, to='volunteering.Message', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('first_name', models.CharField(db_index=True, max_length=200, blank=True)),
                ('surname', models.CharField(max_length=200, db_index=True)),
                ('dear_name', models.CharField(help_text=b'Leave blank if same as first name', max_length=200, blank=True)),
                ('external_id', models.CharField(unique=True, max_length=200)),
                ('email_address', models.EmailField(max_length=75, blank=True)),
                ('home_phone', models.CharField(max_length=200, blank=True)),
                ('mobile_phone', models.CharField(max_length=200, blank=True)),
                ('slug', models.CharField(unique=True, max_length=10, blank=True)),
                ('last_summary_view', models.DateTimeField(null=True)),
                ('note', models.TextField(blank=True)),
                ('temporary_change', models.BooleanField(default=False, db_index=True)),
                ('attributes', models.ManyToManyField(to='volunteering.Attribute', null=True, blank=True)),
                ('family', models.ForeignKey(to='volunteering.Family')),
            ],
            options={
                'ordering': ['surname'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sendable',
            name='volunteer',
            field=models.ForeignKey(to='volunteering.Volunteer'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='sendable',
            unique_together=set([('send_date', 'trigger_type', 'trigger_id', 'volunteer', 'assignment')]),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('name', 'date')]),
        ),
        migrations.AddField(
            model_name='duty',
            name='assignments',
            field=models.ManyToManyField(to='volunteering.Volunteer', through='volunteering.Assignment', db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='duty',
            name='event',
            field=models.ForeignKey(blank=True, to='volunteering.Event', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='duty',
            name='location',
            field=models.ForeignKey(blank=True, to='volunteering.Location', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='duty',
            unique_together=set([('activity', 'event', 'location', 'start_time', 'end_time')]),
        ),
        migrations.AddField(
            model_name='campaign',
            name='events',
            field=models.ManyToManyField(to='volunteering.Event', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='locations',
            field=models.ManyToManyField(to='volunteering.Location', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='assigned_location',
            field=models.ForeignKey(blank=True, to='volunteering.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='duty',
            field=models.ForeignKey(to='volunteering.Duty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='volunteer',
            field=models.ForeignKey(to='volunteering.Volunteer'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([('volunteer', 'duty')]),
        ),
        migrations.AddField(
            model_name='activity',
            name='attributes',
            field=models.ManyToManyField(to='volunteering.Attribute', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DutyEditable',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Duties (editable)',
            },
            bases=('volunteering.duty',),
        ),
    ]
