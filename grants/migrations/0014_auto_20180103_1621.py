# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0013_program_show_names_before_scoring'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['question']},
        ),
        migrations.AddField(
            model_name='question',
            name='sort_priority',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(max_length=50, choices=[(b'boolean', b'Yes/No'), (b'boolean_sortpriority', b'Yes/No with sort priority'), (b'text', b'Short text'), (b'textarea', b'Long text'), (b'integer', b'Integer value')]),
        ),
    ]
