# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userdata_apikey'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='email',
            field=models.CharField(default=b'DEFAULT_VALUE', unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userdata',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userdata',
            name='password',
            field=models.CharField(default=1, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
