from __future__ import annotations

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "email",
                    models.EmailField(
                        unique=True,
                        max_length=75,
                        verbose_name="Email Address",
                        blank=True,
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="Staff status"),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Active"),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="Date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        to="auth.Group", verbose_name="groups", blank=True
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        to="auth.Permission",
                        verbose_name="user permissions",
                        blank=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
    ]
