from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grants", "0008_program_users"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedCSV",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("csv", models.BinaryField(editable=False)),
                ("uploaded", models.DateTimeField(auto_now_add=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
