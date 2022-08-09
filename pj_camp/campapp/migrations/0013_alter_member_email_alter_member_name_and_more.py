# Generated by Django 4.0.6 on 2022-08-09 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campapp', '0012_board_alter_notice_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.TextField(max_length=60, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='password1',
            field=models.TextField(max_length=40),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.TextField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='count',
            field=models.IntegerField(),
        ),
    ]