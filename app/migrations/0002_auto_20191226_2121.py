# Generated by Django 3.0.1 on 2019-12-26 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friendly_name',
            field=models.CharField(default="", max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='slack_id',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='splitwise_id',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
