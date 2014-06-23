# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0002_question_required'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='email',
            field=models.EmailField(max_length=75),
        ),
    ]
