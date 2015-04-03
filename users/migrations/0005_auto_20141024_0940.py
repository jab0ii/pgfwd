# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20141024_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='apiKey',
            field=models.CharField(default=b'DEFAULTx', unique=True, max_length=255),
        ),
    ]
