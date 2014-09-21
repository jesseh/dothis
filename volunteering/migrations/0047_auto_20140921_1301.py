# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


class Migration(migrations.Migration):

    def generic_trigger(apps, schema_editor):
        ContentType = apps.get_model('contenttypes', 'ContentType')
        Sendable = apps.get_model("volunteering", "Sendable")

        try:
            trigger_type = ContentType.objects.get(model='trigger')
        except ObjectDoesNotExist:
            return

        for sendable in Sendable.objects.all():
            sendable.trigger_type = trigger_type
            sendable.trigger_id = sendable.orig_trigger_id
            sendable.save()

    dependencies = [
        ('volunteering', '0046_auto_20140921_1258'),
    ]

    operations = [
        migrations.RunPython(generic_trigger),
    ]
