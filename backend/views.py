from django.shortcuts import render, get_object_or_404
import logging
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VideoClip, DetectedObject, ClientStatus, Settings
from .serializers import VideoClipSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from .services import send_email_notification
from .forms import SettingsForm

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#Django Views

class VideoClipsView(LoginRequiredMixin, ListView):
    model = VideoClip
    template_name = 'index.html'
    context_object_name = 'videoclips'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_status'] = getattr(self.request, 'client_status', None)
        return context

class VideoDetailView(LoginRequiredMixin, DetailView):
    model = VideoClip
    template_name = 'detail.html'
    context_object_name = 'clip'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_object(self, queryset=None):
        clip_id = self.kwargs.get('clip_id')
        return get_object_or_404(VideoClip, pk=clip_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detected_objects'] = DetectedObject.objects.filter(video=self.object)
        context['client_status'] = getattr(self.request, 'client_status', None)
        return context

class SettingsView(LoginRequiredMixin, UpdateView):
    model = Settings
    form_class = SettingsForm
    template_name = 'settings.html'
    context_object_name = 'settings'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_object(self, queryset=None):
        return Settings.objects.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_status'] = getattr(self.request, 'client_status', None)
        return context
    
    def get_success_url(self):
        return reverse_lazy('settings')
    
# Django Rest Framework ViewSets

class VideoClipViewSet(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer

class ClientPing(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client_status, created = ClientStatus.objects.get_or_create()
        logger.debug(f"Client Status: {client_status}")
        client_status.is_up = True
        client_status.last_ping = timezone.now()
        client_status.save()
        return Response(status=status.HTTP_200_OK)

def test_mail(request):
    send_email_notification()