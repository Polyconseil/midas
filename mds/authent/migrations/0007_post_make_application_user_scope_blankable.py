# Generated by Django 2.2.7 on 2019-11-27 13:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authent", "0006_post_fill_allowed_scopes_with_default_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="users_allowed_scopes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=32),
                blank=True,
                default=list,
                help_text="User's allowed scopes (separated with commas)",
                size=None,
            ),
        ),
    ]