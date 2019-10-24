# Generated by Django 2.2 on 2019-10-18 07:50
import json
import uuid

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations


def fill_published_policies_geographies(apps, schema_editor):
    Policy = apps.get_model("mds", "Policy")
    Area = apps.get_model("mds", "Area")

    # A copy of Policy.publish() (don't import models in a migration)
    for policy in Policy.objects.filter(published_date__isnull=False).iterator():
        for rule in policy.rules:
            for area_id in rule["geographies"]:
                area = Area.objects.get(pk=area_id)
                # Generate a new UUID, this is not longer the original area object
                geo_id = uuid.uuid4()
                policy.geographies[str(geo_id)] = {
                    "type": "Feature",
                    "geometry": {
                        "type": "GeometryCollection",
                        "geometries": [
                            json.loads(polygon.geom.geojson)
                            for polygon in area.polygons.all()
                        ],
                    },
                    "id": geo_id,
                    "properties": {
                        "name": area.label,
                        "label": area.label,
                        "area": area_id,
                    },
                }

        policy.save()


class Migration(migrations.Migration):

    dependencies = [("mds", "0057_pre_policy_geographies_add")]

    operations = [
        # Just added the DjangoJSONEncoder
        migrations.AlterField(
            model_name="policy",
            name="geographies",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=django.core.serializers.json.DjangoJSONEncoder,
                null=True,
            ),
        ),
        migrations.RunPython(
            fill_published_policies_geographies, reverse_code=migrations.RunPython.noop
        ),
    ]