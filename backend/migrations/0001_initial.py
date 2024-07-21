# Generated by Django 5.0.6 on 2024-07-21 02:15

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('detection_confidence', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.videoclip')),
            ],
        ),
    ]
