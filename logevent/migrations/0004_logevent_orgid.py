# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logevent', '0003_auto_20141106_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='logevent',
            name='orgID',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
