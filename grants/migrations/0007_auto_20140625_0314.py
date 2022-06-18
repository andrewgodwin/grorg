from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grants", "0006_auto_20140625_0139"),
    ]

    operations = [
        migrations.CreateModel(
            name="Allocation",
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
                ("amount", models.PositiveIntegerField()),
                (
                    "applicant",
                    models.ForeignKey(to="grants.Applicant", on_delete=models.CASCADE),
                ),
                (
                    "resource",
                    models.ForeignKey(to="grants.Resource", on_delete=models.CASCADE),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="allocation",
            unique_together={("applicant", "resource")},
        ),
    ]
