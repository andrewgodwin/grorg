from __future__ import annotations

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("grants", "0009_uploadedcsv"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="join_code",
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="allocation",
            name="applicant",
            field=models.ForeignKey(
                related_name="allocations",
                to="grants.Applicant",
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="allocation",
            name="resource",
            field=models.ForeignKey(
                related_name="allocations",
                to="grants.Resource",
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="answer",
            name="applicant",
            field=models.ForeignKey(
                related_name="answers", to="grants.Applicant", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                related_name="answers", to="grants.Question", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="applicant",
            name="program",
            field=models.ForeignKey(
                related_name="applicants", to="grants.Program", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="question",
            name="program",
            field=models.ForeignKey(
                related_name="questions", to="grants.Program", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="resource",
            name="program",
            field=models.ForeignKey(
                related_name="resources", to="grants.Program", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="score",
            name="applicant",
            field=models.ForeignKey(
                related_name="scores", to="grants.Applicant", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="score",
            name="score",
            field=models.FloatField(
                help_text="From 1 (terrible) to 5 (excellent)", null=True, blank=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="score",
            name="user",
            field=models.ForeignKey(
                related_name="scores",
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
    ]
