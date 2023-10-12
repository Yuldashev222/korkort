def lesson_image_location(instance, image):
    return f'chapters/{str(instance.chapter).replace(" ", "_")}/lessons/{str(instance)}/images/{image}'


def lesson_video_location(instance, video):
    return f'chapters/{str(instance.lesson.chapter).replace(" ", "_")}/lessons/{str(instance)}/videos/{video}'
