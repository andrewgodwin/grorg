from __future__ import annotations

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grants", "0007_auto_20140625_0314"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="users",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
