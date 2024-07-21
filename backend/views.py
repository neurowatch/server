from django.shortcuts import render, get_object_or_404
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import VideoClip, DetectedObject
from .serializers import VideoClipSerializer
from rest_framework.parsers import JSONParser

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Django Views

def index(request):
    videoclips = VideoClip.objects.all()
    return render(
        request,
        'index.html',
        context = {
            "videoclips" : videoclips
        }
    )

def video_detail(request, clip_id):
    videoclip = get_object_or_404(VideoClip, pk=clip_id)
    detectedObjects = DetectedObject.objects.filter(video = videoclip)
    return render(
        request,
        'detail.html',
        context = {
            "clip" : videoclip,
            "detectedObjects" : detectedObjects
        }
    )

def settings(request):
    pass

# Django Rest Framework ViewSets

class VideoClipViewSet(viewsets.ModelViewSet):
    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer