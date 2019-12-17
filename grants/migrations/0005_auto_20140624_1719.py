# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grants', '0004_auto_20140624_0435'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(null=True, blank=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('score_history', models.TextField(null=True, blank=True)),
                ('applicant', models.ForeignKey(to='grants.Applicant', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([(b'applicant', b'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([(b'applicant', b'question')]),
        ),
    ]
