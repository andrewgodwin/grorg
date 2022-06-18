from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grants", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="required",
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
