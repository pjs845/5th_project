# Generated by Django 4.1 on 2022-08-06 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campapp", "0003_notice_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member", name="rdate", field=models.DateTimeField(),
        ),
    ]