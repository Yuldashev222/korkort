def category_image_location(instance, image):
    return f'categories/{str(instance)}/images/{image}'


def question_video_location(instance, video):
    return f'questions/{str(instance)}/videos/{video}'


def question_image_location(instance, image):
    return f'questions/{str(instance)}/images/{image}'

