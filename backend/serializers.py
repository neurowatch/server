from rest_framework import serializers
from .models import VideoClip, VideoInformation

class VideoInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInformation
        fields = ['id', 'object_name', 'detection_confidence']

class VideoClipSerializer(serializers.ModelSerializer):
    video_information = VideoInformationSerializer(many=True, read_only=False)

    class Meta:
        model = VideoClip
        fields = ['id', 'video', 'video_information']

    def create(self, validated_data):
        video_information_data = validated_data.pop('video_information')
        video_clip = VideoClip.objects.create(**validated_data)
        for video_info_data in video_information_data:
            VideoInformation.objects.create(video=video_clip, **video_info_data)
        return video_clip