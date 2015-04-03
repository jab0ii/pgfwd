# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20141024_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
