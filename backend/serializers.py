from .models import VideoClip, DetectedObject, Settings
from .usecases import create_video_clip, generate_thumbnail, create_detected_objects, send_email_notification, send_push_notification
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from rest_framework import serializers
import ffmpeg
import json
import logging
import os
import tempfile


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DetectedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedObject
        fields = ['object_name', 'detection_confidence']

class VideoClipSerializer(serializers.Serializer):

    video = serializers.FileField()
    detected_objects = DetectedObjectSerializer(many=True, write_only=True)
    thumbnail = serializers.FileField(required=False)
    date = serializers.DateTimeField(required=False, read_only=True)

    def create(self, validated_data):
        detected_objects = validated_data.pop('detected_objects')        
        video = validated_data["video"][0]
        video_clip = create_video_clip(video=video)
        generate_thumbnail(video_clip)
        create_detected_objects(video_clip, detected_objects)
        send_email_notification(video_clip)
        send_push_notification(video_clip)

        return video_clip        
    
    def to_internal_value(self, data):
        if not "detected_objects" in data.keys():
            raise serializers.ValidationError(
                {"detected_objects" : "This field is required"}
            )
        return data