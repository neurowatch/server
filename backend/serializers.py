import ffmpeg
import os
import io
from rest_framework import serializers
from .models import VideoClip, VideoInformation
from django.core.exceptions import ValidationError
from django.conf import settings
import logging
import json
import tempfile
from django.core.files import File

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
        fields = ['id', 'video', 'thumbnail', 'date', 'video_information']
        extra_kwargs = {
            'thumbnail': {'required': False}
        }

    def create(self, validated_data):

        logger.debug("------------------------")
        logger.debug("------------------------")
        logger.debug(validated_data)

        video_clip = VideoClip.objects.create(**validated_data)
        self.generate_thumbnail(video_clip)

        try:
            metadata = self.extract_metadata(video_clip.video)
        except ValidationError as e:
            logger.error(e)
            raise serializers.ValidationError({'video': str(e)})
        except Exception as e:
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
        
    def generate_thumbnail(self, video):
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                thumb_temp_path = temp_file.name                
                ffmpeg.input(video.video.path).filter('select', 'eq(n,0)').output(thumb_temp_path, vframes=1).overwrite_output().run()

            logger.debug("-----------------")
            logger.debug(thumb_temp_path)
            logger.debug("-----------------")

            with open(thumb_temp_path, 'rb') as temp_file:
                thumb_file = File(temp_file)
                video.thumbnail.save(os.path.basename(thumb_temp_path), thumb_file, save=True)

            os.remove(thumb_temp_path)
        except Exception as e:
            logger.error(e)
            raise e
