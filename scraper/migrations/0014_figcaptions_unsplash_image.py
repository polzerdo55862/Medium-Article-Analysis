# Generated by Django 3.2.4 on 2021-08-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0013_auto_20210823_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='figcaptions',
            name='unsplash_image',
            field=models.BooleanField(default=False),
        ),
    ]
