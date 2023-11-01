import os

from moviepy.editor import VideoFileClip


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
    try:
        old_file = getattr(model_class.objects.get(pk=instance.pk), field_name)
    except model_class.DoesNotExist:
        return
    instance_file = getattr(instance, field_name)
    if instance_file and old_file and instance_file != old_file and os.path.isfile(old_file.path):
        os.remove(old_file.path)


def bubble_search(field_id, field_name, sort_list):
    len_list = len(sort_list)
    left, right = 0, len_list - 1

    while left <= right:
        mid = (left + right) // 2
        temp = sort_list[mid]
        if temp[field_name] == field_id:
            return temp
        elif temp[field_name] < field_id:
            left = mid + 1
        else:
            right = mid - 1

    return None
