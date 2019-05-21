# Generated by Django 2.1.7 on 2019-05-21 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("authent", "0002_auto_20190124_0928")]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="owner",
            field=models.UUIDField(
                blank=True,
                db_index=True,
                help_text="Unique identifier for the owner of the application",
                null=True,
            ),
        )
    ]
