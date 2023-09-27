import os

import requests
from moviepy.editor import VideoFileClip


def get_language():
    from django.utils.translation import get_language
    return str(get_language()).replace('-', '_')


def get_video_duration(video_path):
    try:
        with VideoFileClip(video_path) as video:
            return round(video.duration / 60, 1)
    except Exception as e:
        print(e)
        return 0


def delete_object_file_post_delete(instance, field_name):
    file = getattr(instance, field_name)
    if file and os.path.isfile(file.path):
        os.remove(file.path)


def delete_object_file_pre_save(model_class, instance, field_name):
    old_file = getattr(model_class.objects.get(id=instance.id), field_name)
    instance_file = getattr(instance, field_name)
    if instance_file and instance_file != old_file and os.path.isfile(old_file.path):
        os.remove(old_file.path)

