from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from backend.models import ClientStatus

class Command(BaseCommand):
    help = "Updates client status"

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timedelta(minutes=1)
        ClientStatus.objects.filter(last_ping__lt=threshold).update(is_up=False)
        self.stdout.write(self.style.SUCCESS('CameraClient status is updated'))