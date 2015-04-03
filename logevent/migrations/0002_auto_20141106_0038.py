# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logevent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logevent',
            name='date_ack',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='logevent',
            name='date_created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='logevent',
            name='date_sent',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='logevent',
            name='log_type',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='logevent',
            name='time_diff',
            field=models.DecimalField(null=True, max_digits=100, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='logevent',
            name='uuid',
            field=models.CharField(max_length=36),
        ),
    ]
