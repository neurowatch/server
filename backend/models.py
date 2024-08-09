from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class VideoClip(models.Model):
    video = models.FileField(upload_to='videos/')
    date = models.DateTimeField(auto_now_add=True)
    thumbnail = models.FileField(upload_to='thumbs/')

class DetectedObject(models.Model):
    video = models.ForeignKey(VideoClip, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=100)
    detected_in_frame = models.IntegerField()
    timestamp = models.IntegerField()
    detection_confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

class ClientStatus(models.Model):
    is_up = models.BooleanField(default=False)
    last_ping = models.DateTimeField(auto_now_add=True)

class Settings(models.Model):
    emails_enabled = models.BooleanField(default=True)
    push_notification_enabled = models.BooleanField(default=True)
    recipient_address = models.EmailField()