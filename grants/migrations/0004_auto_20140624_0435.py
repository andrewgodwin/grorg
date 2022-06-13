# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0003_auto_20140623_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(max_length=50, choices=[('boolean', 'Yes/No'), ('text', 'Short text'), ('textarea', 'Long text'), ('integer', 'Integer value')]),
        ),
        migrations.AlterUniqueTogether(
            name='applicant',
            unique_together=set([('program', 'email')]),
        ),
    ]
