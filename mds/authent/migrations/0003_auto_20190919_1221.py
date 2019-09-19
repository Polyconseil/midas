# Generated by Django 2.1.12 on 2019-09-19 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mds', '0045_auto_20190919_1221'),
        ('authent', '0002_auto_20190124_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='aggregator_for',
            field=models.ManyToManyField(help_text='Provider the application is allowed to write for', to='mds.Provider'),
        ),
        migrations.AlterField(
            model_name='application',
            name='owner',
            field=models.UUIDField(blank=True, db_index=True, help_text='Unique identifier for the owner of the application', null=True),
        ),
    ]
