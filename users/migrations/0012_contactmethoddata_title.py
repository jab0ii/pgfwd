# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20141105_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmethoddata',
            name='title',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
