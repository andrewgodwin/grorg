# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0012_auto_20160119_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='show_names_before_scoring',
            field=models.BooleanField(default=True, help_text=b"Show applicant's name and email even before scoring."),
        ),
    ]
