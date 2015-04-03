# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_ack', models.DateTimeField(default=django.utils.timezone.now)),
                ('log_type', models.IntegerField()),
                ('time_diff', models.IntegerField(blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
