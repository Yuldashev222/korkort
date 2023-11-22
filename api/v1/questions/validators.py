from django.conf import settings
from django.core.exceptions import ValidationError


def validate_question_video_size(video_obj):
    if video_obj.file.size > settings.MAX_QUESTION_VIDEO_UPLOAD_SIZE:
        raise ValidationError("Max file size is %sMB" % str(settings.MAX_QUESTION_VIDEO_UPLOAD_SIZE))
