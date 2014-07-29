# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0004_auto_20140729_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='deactivate_date',
            field=models.DateTimeField(help_text='keep empty for indefinite activation', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='activate_date',
            field=models.DateTimeField(help_text='keep empty for an immediate activation', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campaign',
            name='status',
            field=models.IntegerField(default=1, verbose_name='status', choices=[(0, 'Inactive'), (1, 'Active')]),
            preserve_default=True,
        ),
    ]
