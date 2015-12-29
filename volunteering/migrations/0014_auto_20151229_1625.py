# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0013_auto_20150915_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='attributes',
            field=models.ManyToManyField(to='volunteering.Attribute', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='activities',
            field=models.ManyToManyField(to='volunteering.Activity', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='bcc_address',
            field=models.EmailField(help_text=b'BCC selected campaign emails to this address.', max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='events',
            field=models.ManyToManyField(to='volunteering.Event', blank=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='locations',
            field=models.ManyToManyField(to='volunteering.Location', blank=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='attributes',
            field=models.ManyToManyField(to='volunteering.Attribute', blank=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='email_address',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
