# Generated by Django 2.1.7 on 2019-03-01 11:13

from django.db import migrations
import mds.models


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0010_device_dn_battery_pct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='label',
            field=mds.models.UnboundedCharField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='polygon',
            name='label',
            field=mds.models.UnboundedCharField(blank=True, db_index=True, null=True),
        ),
    ]
