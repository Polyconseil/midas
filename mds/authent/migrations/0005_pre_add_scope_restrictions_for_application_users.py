# Generated by Django 2.2.7 on 2019-11-26 09:32

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authent", "0004_post_fill_default_aggregator_for"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="users_allowed_scopes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=32),
                null=True,
                help_text="User's allowed scopes (separated with commas)",
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="application",
            name="aggregator_for",
            field=models.ManyToManyField(
                blank=True,
                help_text="Provider the application is allowed to write for",
                to="mds.Provider",
            ),
        ),
    ]
