# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
