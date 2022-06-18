from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grants", "0010_auto_20150320_1734"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="duplicate_emails",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="email",
            field=models.EmailField(max_length=254),
        ),
    ]
