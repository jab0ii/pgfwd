# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20141024_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='email',
            field=models.CharField(unique=True, max_length=100),
        ),
    ]
