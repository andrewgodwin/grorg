from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                related_query_name="user",
                related_name="user_set",
                to="auth.Group",
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of his/her group.",
                verbose_name="groups",
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                related_query_name="user",
                related_name="user_set",
                to="auth.Permission",
                blank=True,
                help_text="Specific permissions for this user.",
                verbose_name="user permissions",
            ),
            preserve_default=True,
        ),
    ]
