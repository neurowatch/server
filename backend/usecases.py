import ffmpeg
import os
import logging
import tempfile
import json
from django.core.files import File
from .models import VideoClip, DetectedObject, Settings, FCMToken
from .services import send_email, send_push

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_video_clip(video):
    '''
        Saves the video clip
    '''
    video_clip = VideoClip.objects.create(video=video)
    return video_clip

def generate_thumbnail(video_clip):
    '''
        Uses the first frame of the video as thumbnail
    '''
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            thumb_temp_path = temp_file.name                
            ffmpeg.input(video_clip.video.path).filter('select', 'eq(n,0)').output(thumb_temp_path, vframes=1).overwrite_output().run()

        with open(thumb_temp_path, 'rb') as temp_file:
            thumb_file = File(temp_file)
            video_clip.thumbnail.save(os.path.basename(thumb_temp_path), thumb_file, save=True)

        os.remove(thumb_temp_path)
    except Exception as e:
        logger.error(e)
        raise 
        
def create_detected_objects(video_clip, detected_objects):
    '''
        Saves the detected objects from the video clip
    '''

    for detected_object in detected_objects:
        # The detected objects are being returned as an array of json strings that need to be parsed 
        detected_object = json.loads(detected_object.replace("'", "\""))
        DetectedObject.objects.create(
            video=video_clip, 
            object_name=detected_object["object_name"], 
            detection_confidence=detected_object["detection_confidence"],
            detected_in_frame=detected_object["detected_in_frame"],
            timestamp = obtain_timestamp(video_clip, detected_object["detected_in_frame"])
        )

def obtain_timestamp(video_clip, frame_number):
    '''
        Gets the video duration from the frame rate
    '''
    probe = ffmpeg.probe(video_clip.video.path)
    frame_rate = 0
    for stream in probe["streams"]:
        if stream["codec_type"] == "video":
            frame_rate = eval(stream["r_frame_rate"])
            break
    
    timestamp = frame_number / frame_rate
    return timestamp

def send_email_notification(video_clip):
    '''
        Sends an email if the email notifications are enabled
    '''
    settings = Settings.objects.first()
    if settings.emails_enabled:
        send_email(settings.recipient_address, video_clip.id)

def send_push_notification(video_clip):
    '''
        Sends a push notification if the push notifications are enabled
    '''
    settings = Settings.objects.first()
    if settings.push_notification_enabled:
        token = FCMToken.objects.first()
        send_push(token)