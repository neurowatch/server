from .models import DetectedObject, VideoClip
from .usecases import create_video_clip, generate_thumbnail, create_detected_objects, send_email_notification, send_push_notification
from rest_framework import serializers
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

'''
    The serializers are used by the django rest framework views to handle the requests.
'''

class DetectedObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedObject
        fields = ['object_name', 'detection_confidence']

class VideoClipSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    video = serializers.FileField()
    detected_objects = DetectedObjectSerializer(many=True, write_only=True)
    thumbnail = serializers.FileField(required=False)
    date = serializers.DateTimeField(required=False, read_only=True)

    class Meta:
        model = VideoClip
        fields = ['id', 'video', 'date', 'thumbnail']

    def create(self, validated_data):
        # Extract the detected objects
        detected_objects = validated_data.pop('detected_objects')        
        video = validated_data["video"][0]
        # Save the video clip object and thumbnail
        video_clip = create_video_clip(video=video)
        generate_thumbnail(video_clip)

        # Save the detected objects 
        create_detected_objects(video_clip, detected_objects)

        # Send notifications
        send_email_notification(video_clip)
        send_push_notification(video_clip)

        return video_clip        
    
    def to_internal_value(self, data):
        if not "detected_objects" in data.keys():
            raise serializers.ValidationError(
                {"detected_objects" : "This field is required"}
            )
        return data