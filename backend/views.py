from django.shortcuts import render
from rest_framework import viewsets
from .models import VideoClip
from .serializers import VideoClipSerializer

class VideoClipViewSet(viewsets.ModelViewSet):
    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer