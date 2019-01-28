# Generated by Django 2.1.5 on 2019-01-28 15:25

import django.contrib.postgres.fields.hstore
from django.contrib.postgres.operations import HStoreExtension
from django.db import migrations
import mds.models


class Migration(migrations.Migration):

    dependencies = [("mds", "0006_provider_device_category")]

    operations = [
        HStoreExtension(),
        migrations.AddField(
            model_name="provider",
            name="authentication",
            field=django.contrib.postgres.fields.hstore.HStoreField(
                default=dict, verbose_name="API Authentication"
            ),
        ),
        migrations.AddField(
            model_name="provider",
            name="base_api_url",
            field=mds.models.UnboundedCharField(
                default="", verbose_name="Base API URL"
            ),
        ),
    ]
