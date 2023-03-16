from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grants", "0002_question_required"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applicant",
            name="email",
            field=models.EmailField(max_length=75),
        ),
    ]
