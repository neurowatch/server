from django.shortcuts import render
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

# Django Rest Framework ViewSets
class VideoClipViewSet(viewsets.ModelViewSet):
    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer