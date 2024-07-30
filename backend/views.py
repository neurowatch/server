from django.shortcuts import render, get_object_or_404
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import VideoClip, DetectedObject
from .serializers import VideoClipSerializer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .services import send_email_notification

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Django Views

class VideoClipsView(LoginRequiredMixin, ListView):
    model = VideoClip
    template_name = 'index.html'
    context_object_name = 'videoclips'
    login_url = "/login/"
    redirect_field_name = "redirect_to"

class VideoDetailView(LoginRequiredMixin, DetailView):
    model = VideoClip
    template_name = 'detail.html'
    context_object_name = 'clip'
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get_object(self, queryset=None):
        clip_id = self.kwargs.get('pk')
        return get_object_or_404(VideoClip, pk=clip_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detectedObjects'] = DetectedObject.objects.filter(video=self.object)
        return context

'''
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

'''

def settings(request):
    pass

# Django Rest Framework ViewSets

class VideoClipViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer

def test_mail(request):
    send_email_notification()