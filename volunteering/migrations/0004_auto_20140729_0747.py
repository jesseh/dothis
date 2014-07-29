# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0003_auto_20140728_2232'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together=set([(b'volunteer', b'campaign_duty')]),
        ),
    ]
