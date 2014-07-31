# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('short_description', models.TextField(null=True, blank=True)),
            ],
            options={
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
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='attributes',
            field=models.ManyToManyField(to='volunteering.Attribute', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('status', models.IntegerField(default=1, verbose_name='status', choices=[(0, 'Inactive'), (1, 'Active')])),
                ('activate_date', models.DateTimeField(help_text='keep empty for an immediate activation', null=True, blank=True)),
                ('deactivate_date', models.DateTimeField(help_text='keep empty for indefinite activation', null=True, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': (b'status', b'-activate_date'),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CampaignDuty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('campaign', models.ForeignKey(to='volunteering.Campaign')),
            ],
            options={
                'ordering': (b'-modified', b'-created'),
                'abstract': False,
                'get_latest_by': b'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.TimeField(null=True, blank=True)),
                ('end_time', models.TimeField(null=True, blank=True)),
                ('multiple', models.IntegerField(default=1, help_text=b'The number of volunteers needed for this duty.')),
                ('activity', models.ForeignKey(blank=True, to='volunteering.Activity', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='campaignduty',
            name='duty',
            field=models.ForeignKey(to='volunteering.Duty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assignment',
            name='duty',
            field=models.ForeignKey(to='volunteering.Duty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='duty',
            name='campaign',
            field=models.ManyToManyField(to='volunteering.Campaign', null=True, through='volunteering.CampaignDuty', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('short_description', models.TextField(null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='duty',
            name='event',
            field=models.ForeignKey(blank=True, to='volunteering.Event', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([(b'name', b'date')]),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('short_description', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='duty',
            name='location',
            field=models.ForeignKey(blank=True, to='volunteering.Location', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('external_id', models.CharField(max_length=200, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=200, null=True, blank=True)),
                ('slug', models.CharField(unique=True, max_length=10, blank=True)),
                ('attributes', models.ManyToManyField(to='volunteering.Attribute', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='duty',
            name='assignments',
            field=models.ManyToManyField(to='volunteering.Volunteer', through='volunteering.Assignment'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='duty',
            unique_together=set([(b'activity', b'event', b'location')]),
        ),
        migrations.AddField(
            model_name='assignment',
            name='volunteer',
            field=models.ForeignKey(to='volunteering.Volunteer'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([(b'volunteer', b'duty')]),
        ),
    ]
