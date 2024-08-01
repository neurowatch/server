from .models import VideoClip, DetectedObject, Settings
from .services import send_email_notification
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
        video_clip = VideoClip.objects.create(video=video)
        self.generate_thumbnail(video_clip)
        for detectedObject in detected_objects:
            detectedObject = json.loads(detectedObject.replace("'", "\""))
            DetectedObject.objects.create(video=video_clip, object_name=detectedObject["object_name"], detection_confidence=detectedObject["detection_confidence"])

        settings = Settings.objects.first()

        if settings.emails_enabled:
            send_email_notification(settings.recipient_address, video_clip.id)
        
        if settings.push_notification_enabled:
            pass

        return video_clip        
    
    def to_internal_value(self, data):
        if not "detected_objects" in data.keys():
            raise serializers.ValidationError(
                {"detected_objects" : "This field is required"}
            )
        return data
        
    def generate_thumbnail(self, video):
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                thumb_temp_path = temp_file.name                
                ffmpeg.input(video.video.path).filter('select', 'eq(n,0)').output(thumb_temp_path, vframes=1).overwrite_output().run()

            with open(thumb_temp_path, 'rb') as temp_file:
                thumb_file = File(temp_file)
                video.thumbnail.save(os.path.basename(thumb_temp_path), thumb_file, save=True)

            os.remove(thumb_temp_path)
        except Exception as e:
            logger.error(e)
            raise e