# Generated by Django 3.2.4 on 2021-07-03 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googleapi', '0003_alter_teachers_credentials'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachers',
            name='credentials',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
