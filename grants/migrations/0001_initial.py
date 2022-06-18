from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Answer",
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
                ("answer", models.TextField()),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Applicant",
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
                ("name", models.TextField()),
                ("email", models.TextField()),
                ("applied", models.DateTimeField(null=True, blank=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="answer",
            name="applicant",
            field=models.ForeignKey(
                to="grants.Applicant", to_field="id", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name="Program",
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
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("applications_open", models.DateTimeField(null=True, blank=True)),
                ("applications_close", models.DateTimeField(null=True, blank=True)),
                ("grants_announced", models.DateTimeField(null=True, blank=True)),
                ("program_starts", models.DateTimeField(null=True, blank=True)),
                ("completed", models.BooleanField(default=False)),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="applicant",
            name="program",
            field=models.ForeignKey(
                to="grants.Program", to_field="id", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name="Question",
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
                (
                    "type",
                    models.CharField(
                        max_length=50,
                        choices=[
                            ("boolean", "Yes/No"),
                            ("text", "Text"),
                            ("integer", "Integer value"),
                        ],
                    ),
                ),
                ("question", models.TextField()),
                ("order", models.IntegerField(default=0)),
                (
                    "program",
                    models.ForeignKey(
                        to="grants.Program", to_field="id", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                to="grants.Question", to_field="id", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name="Resource",
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
                ("name", models.CharField(max_length=100)),
                (
                    "type",
                    models.CharField(
                        max_length=50,
                        choices=[
                            ("money", "Money"),
                            ("ticket", "Ticket"),
                            ("place", "Place"),
                            ("accomodation", "Accomodation"),
                        ],
                    ),
                ),
                (
                    "program",
                    models.ForeignKey(
                        to="grants.Program", to_field="id", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ResourceDonation",
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
                ("amount", models.IntegerField()),
                ("source", models.TextField(null=True, blank=True)),
                (
                    "resource",
                    models.ForeignKey(
                        to="grants.Resource", to_field="id", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
