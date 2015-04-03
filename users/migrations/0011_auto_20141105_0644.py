# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20141025_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmethoddata',
            name='priority',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='contactmethoddata',
            unique_together=set([('user', 'priority')]),
        ),
    ]
