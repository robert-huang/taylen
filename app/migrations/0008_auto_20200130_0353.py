# Generated by Django 3.0.2 on 2020-01-30 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_emoji_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emoji',
            name='image_url',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
