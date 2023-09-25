from PIL import Image


def category_image_location(instance, image):
    return f'categories/{str(instance).replace(" ", "_")}/images/{image}'


def question_gif_location(instance, gif):
    return f'questions/{str(instance).replace(" ", "_")}/gifs/{gif}'


def question_image_location(instance, image):
    return f'questions/{str(instance).replace(" ", "_")}/images/{image}'


def get_last_frame_number_and_duration(gif_path):
    try:
        with Image.open(gif_path) as img:
            last_frame_number = img.n_frames - 1
            duration = 0
            if img.is_animated:
                duration = round(img.info.get("duration", 0) / 1000.0, 2)

            return duration, last_frame_number
    except Exception as e:
        print(e)
        return 0, 0


# pt = '/home/oybek/Downloads/11xHTywJSoZIMTgyfgFLBJQ-1.gif'
#
# print(get_last_frame_number_and_duration(pt))
