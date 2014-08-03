# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0008_remove_campaign_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('body', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('when_fixed', models.DateField(null=True, blank=True)),
                ('when_relative', models.PositiveIntegerField(null=True, blank=True)),
                ('campaign', models.ForeignKey(blank=True, to='volunteering.Campaign', null=True)),
                ('message', models.ForeignKey(blank=True, to='volunteering.Message', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='duty',
            name='multiple',
            field=models.PositiveIntegerField(default=1, help_text=b'The number of volunteers needed for this duty.'),
        ),
    ]
