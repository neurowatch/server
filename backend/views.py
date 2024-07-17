from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import VideoClip
from .serializers import VideoClipSerializer

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
    return render(
        request,
        'detail.html',
        context = {
            "clip" : videoclip
        }
    )

def settings(request):
    pass

# Django Rest Framework ViewSets
class VideoClipViewSet(viewsets.ModelViewSet):
    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer