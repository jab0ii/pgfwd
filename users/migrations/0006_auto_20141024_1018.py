# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20141024_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='org',
            field=models.ForeignKey(blank=True, to='orgs.OrgData', null=True),
        ),
    ]
