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
