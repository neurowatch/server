from django import forms
from .models import Settings

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['emails_enabled', 'push_notification_enabled', 'recipient_address']
