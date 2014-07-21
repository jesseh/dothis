# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('campaign', models.ForeignKey(to='volunteering.Campaign', to_field='id')),
                ('assigned_to', models.ForeignKey(to_field='id', blank=True, to='volunteering.Volunteer', null=True)),
                ('attributes', models.ManyToManyField(to='volunteering.Attribute')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
