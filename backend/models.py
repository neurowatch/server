from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class VideoClip(models.Model):
    video_path = models.CharField(max_length=100)

class VideoInformation(models.Model):
    video = models.ForeignKey(VideoClip, related_name='video_information', on_delete=models.CASCADE)
    object_name = models.CharField(max_length=100)
    detection_confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])