import ffmpeg
import os
import io
from rest_framework import serializers
from .models import VideoClip, VideoInformation
from django.core.exceptions import ValidationError
from django.conf import settings
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoInformation
        fields = ['id', 'object_name', 'detection_confidence']

class VideoClipSerializer(serializers.ModelSerializer):
    video_information = VideoInformationSerializer(many=True, required=False)

    class Meta:
        model = VideoClip
        fields = ['id', 'video', 'video_information']

    def create(self, validated_data):

        logger.debug("------------------------")
        logger.debug(validated_data)

        video_information_data = validated_data.pop('video_information', None)
        if video_information_data:
            for video_info_data in video_information_data:
                VideoInformation.objects.create(video=video_clip, **video_info_data)

        video_clip = VideoClip.objects.create(**validated_data)

        try:
            metadata = self.extract_metadata(video_clip.video)
        except ValidationError as e:
            logger.error(e)
            raise serializers.ValidationError({'video': str(e)})

        for info in metadata:
            VideoInformation.objects.create(video=video_clip, **info)

        return video_clip
    
    def extract_metadata(self, video):
        try:
            file_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, video.name))

            probe = ffmpeg.probe(filename=file_path)

            metadata = probe.get('format', {}).get('tags', {})
    
            detected_objects = json.loads(metadata['description'])

            logger.debug(detected_objects)
            logger.debug("-----------------")

            return detected_objects

        except Exception as e:
            logger.error(e)
            logger.error(e.stderr)
            raise ValidationError(str(e))