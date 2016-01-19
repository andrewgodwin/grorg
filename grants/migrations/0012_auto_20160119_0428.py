# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0011_auto_20160113_0505'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='applicant',
            unique_together=set([]),
        ),
    ]
