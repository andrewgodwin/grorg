# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grants', '0005_auto_20140624_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourcedonation',
            name='resource',
        ),
        migrations.DeleteModel(
            name='ResourceDonation',
        ),
        migrations.AddField(
            model_name='resource',
            name='amount',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='score',
            name='comment',
            field=models.TextField(help_text=b'Seen only by other voters, not by the applicant', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.FloatField(help_text=b'From 0 (terrible) to 5 (excellent)', null=True, blank=True),
        ),
    ]
