# Generated by Django 2.1.12 on 2019-09-19 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0044_add_compliance_list'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='policy',
            options={'verbose_name_plural': 'policies'},
        ),
        migrations.AddField(
            model_name='policy',
            name='fixed_price',
            field=models.IntegerField(default=0),
        ),
    ]