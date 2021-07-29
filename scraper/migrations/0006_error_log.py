# Generated by Django 3.2.5 on 2021-07-19 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_users_collect_user_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error_Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('reason', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.users')),
            ],
        ),
    ]