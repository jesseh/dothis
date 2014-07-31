# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('campaign', models.ForeignKey(to='volunteering.Campaign')),
                ('event', models.ForeignKey(to='volunteering.Event')),
            ],
            options={
                'ordering': (b'-modified', b'-created'),
                'abstract': False,
                'get_latest_by': b'modified',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='campaignduty',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='campaignduty',
            name='duty',
        ),
        migrations.AddField(
            model_name='campaign',
            name='campaign',
            field=models.ManyToManyField(to=b'volunteering.Event', null=True, through='volunteering.CampaignEvent', blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='duty',
            name='campaign',
        ),
        migrations.DeleteModel(
            name='CampaignDuty',
        ),
    ]
