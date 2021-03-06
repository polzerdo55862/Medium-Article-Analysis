# Generated by Django 3.2.4 on 2021-08-17 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0010_articles_voter_scraped_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Figcaptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=500)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.articles')),
            ],
        ),
    ]
