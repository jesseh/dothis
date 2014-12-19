# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def replace_nulls(apps, schema_editor):
    for model_name in ['Event', 'Activity', 'Location']:
        model = apps.get_model("volunteering", model_name)
        model.objects.filter(
            web_summary_description__isnull=True,
        ).update(web_summary_description="")
        model.objects.filter(
            assignment_message_description__isnull=True,
        ).update(assignment_message_description="")


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0052_auto_20141006_1954'),
    ]

    operations = [
        migrations.RunPython(replace_nulls),
    ]
