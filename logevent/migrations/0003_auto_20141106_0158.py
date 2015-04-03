# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logevent', '0002_auto_20141106_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logevent',
            name='user',
            field=models.IntegerField(null=True),
        ),
    ]
