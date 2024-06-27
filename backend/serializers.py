from rest_framework import serializers
from .models import VideoClip, VideoInformation

class VideoInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInformation
        fields = ['id', 'object_name', 'detection_confidence']

class VideoClipSerializer(serializers.ModelSerializer):
    video_infromation = VideoInformationSerializer(many=True, read_only=True)

    class Meta:
        model = VideoClip,
        fields = ['id', 'video_path', 'video_information']