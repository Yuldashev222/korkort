from PIL import Image


def category_image_location(instance, image):
    return f'categories/{str(instance)}/images/{image}'


def question_gif_location(instance, gif):
    return f'questions/{str(instance)}/gifs/{gif}'


def question_image_location(instance, image):
    return f'questions/{str(instance)}/images/{image}'


def get_last_frame_number(gif_path):
    try:
        with Image.open(gif_path) as img:
            return img.n_frames - 1
    except Exception as e:
        return None
