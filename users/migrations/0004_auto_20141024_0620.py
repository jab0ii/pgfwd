# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20141024_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='apiKey',
            field=models.CharField(default=b'DEFAULT', unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='status',
            field=models.IntegerField(default=4),
        ),
    ]
