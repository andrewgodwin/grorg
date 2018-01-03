# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0012_auto_20160119_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.FloatField(blank=True, help_text=b'From 1 (terrible) to 5 (excellent)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
