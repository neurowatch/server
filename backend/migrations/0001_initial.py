# Generated by Django 4.2.14 on 2024-08-24 21:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_up', models.BooleanField(default=False)),
                ('last_ping', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FCMToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emails_enabled', models.BooleanField(default=True)),
                ('push_notification_enabled', models.BooleanField(default=True)),
                ('recipient_address', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='VideoClip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='videos/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.FileField(upload_to='thumbs/')),
            ],
        ),
        migrations.CreateModel(
            name='DetectedObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_name', models.CharField(max_length=100)),
                ('detected_in_frame', models.IntegerField()),
                ('timestamp', models.IntegerField()),
                ('detection_confidence', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.videoclip')),
            ],
        ),
    ]
