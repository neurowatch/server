from django.contrib import admin
from .models import VideoClip, DetectedObject #, NeurowatchUser
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

# Register your models here.
admin.site.register(VideoClip)
admin.site.register(DetectedObject)
# admin.site.register(NeurowatchUser)

