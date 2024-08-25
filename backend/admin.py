from django.contrib import admin
from .models import VideoClip, DetectedObject, Settings, FCMToken
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

# Register your models here.
admin.site.register(VideoClip)
admin.site.register(DetectedObject)
admin.site.register(Settings)
admin.site.register(FCMToken)
