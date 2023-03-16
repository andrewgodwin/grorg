from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("grants", "0011_auto_20160113_0505"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="applicant",
            unique_together=set(),
        ),
    ]
