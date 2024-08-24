from .forms import SettingsForm
from .models import VideoClip, DetectedObject, ClientStatus, Settings, FCMToken
from .serializers import VideoClipSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView 
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed
import logging

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

    queryset = ClientStatus.objects.get_or_create()

    def post(self, request, *args, **kwargs):
        client_status, created = ClientStatus.objects.get_or_create()
        logger.debug(f"Client Status: {client_status}")
        client_status.is_up = True
        client_status.last_ping = timezone.now()
        client_status.save()
        return Response(status=status.HTTP_200_OK)
    
class APILogin(APIView):

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        logger.debug(f'Sandunga')
        logger.debug(f'{user} {username} {password}')
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Authentication Failed'}, status=status.HTTP_401_UNAUTHORIZED)
        
class SettingsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Settings.objects.all()

    def get_queryset(self):
        # Return a queryset with only the first Settings instance
        return Settings.objects.filter(pk=Settings.objects.first().pk) if Settings.objects.exists() else Settings.objects.none()

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')

class APIFcmToken(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = FCMToken.objects.get_or_create()

    def post(self, request, *args, **kwargs):
        fcmToken, created = FCMToken.objects.get_or_create()
        fcmToken.save()
        return Response(status=status.HTTP_200_OK)

