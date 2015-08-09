# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0005_volunteeradded'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerNotModified',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Recently (not) modified volunteers',
            },
            bases=('volunteering.volunteer',),
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['name'], 'verbose_name_plural': 'Activities'},
        ),
        migrations.AlterModelOptions(
            name='family',
            options={'ordering': ['external_id'], 'verbose_name_plural': 'Families'},
        ),
        migrations.AddField(
            model_name='triggerbyassignment',
            name='bcc',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='triggerbydate',
            name='bcc',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='triggerbyevent',
            name='bcc',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
