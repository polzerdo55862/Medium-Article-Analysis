# Generated by Django 3.2.4 on 2021-08-24 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0015_remove_figcaptions_unsplash_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='figcaptions',
            name='self_made',
        ),
        migrations.RemoveField(
            model_name='figcaptions',
            name='self_made_automated_label',
        ),
    ]