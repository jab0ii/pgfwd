# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventHandlerData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('hierarchy', models.TextField()),
                ('org', models.ForeignKey(to='orgs.OrgData')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
