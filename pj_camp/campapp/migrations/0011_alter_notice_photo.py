# Generated by Django 4.1 on 2022-08-08 17:36

import campapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campapp", "0010_notice_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notice",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to=campapp.models.date_upload_to
            ),
        ),
    ]
