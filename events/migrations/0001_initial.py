# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventhandlers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36)),
                ('title', models.TextField()),
                ('message', models.TextField()),
                ('currentPos', models.IntegerField()),
                ('status', models.IntegerField()),
                ('handler', models.ForeignKey(to='eventhandlers.EventHandlerData')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
