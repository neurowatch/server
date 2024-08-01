# Generated by Django 5.0.6 on 2024-08-01 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_clientstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emails_enabled', models.BooleanField(default=True)),
                ('push_notification_enabled', models.BooleanField(default=True)),
                ('recipient_address', models.EmailField(max_length=254)),
            ],
        ),
    ]
