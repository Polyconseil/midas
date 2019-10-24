# Generated by Django 2.2 on 2019-10-14 13:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("mds", "0056_post_compliance_saved_at_not_nullable")]

    operations = [
        migrations.AddField(
            model_name="policy",
            name="geographies",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                null=True,
            ),
        )
    ]