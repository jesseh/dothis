# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0013_auto_20140804_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('family_id', models.CharField(unique=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='dear_name',
            field=models.CharField(default='', help_text=b'Leave blank if same as first name', max_length=200, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='volunteer',
            name='email_address',
            field=models.EmailField(default='', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='volunteer',
            name='family_id',
            field=models.ForeignKey(to='volunteering.Family', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='volunteer',
            name='first_name',
            field=models.CharField(default='', max_length=200, blank=True),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='volunteer',
            old_name='phone_number',
            new_name='home_phone',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='individual_id',
            field=models.CharField(default='', unique=True, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='volunteer',
            name='mobile_phone',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='volunteer',
            old_name='name',
            new_name='surname',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='title',
            field=models.CharField(default='', max_length=200, blank=True),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='external_id',
        ),
        migrations.RemoveField(
            model_name='volunteer',
            name='slug',
        ),
    ]
