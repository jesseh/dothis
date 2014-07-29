# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0002_campaignduty_duty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('volunteer', models.ForeignKey(to='volunteering.Volunteer', to_field='id')),
                ('campaign_duty', models.ForeignKey(to='volunteering.CampaignDuty', to_field='id')),
            ],
            options={
                'ordering': (b'-modified', b'-created'),
                'abstract': False,
                'get_latest_by': b'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='campaignduty',
            name='assignments',
            field=models.ManyToManyField(to='volunteering.Volunteer', through='volunteering.Assignment'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='campaignduty',
            name='assigned_to',
        ),
    ]
