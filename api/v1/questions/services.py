from PIL import Image, ImageSequence


def get_last_frame_number_and_duration(gif_path):
    try:
        with Image.open(gif_path) as img:
            if not img.is_animated:
                return 0, 0

            duration = 0
            for frame in ImageSequence.Iterator(img):
                duration += frame.info.get("duration", 0)
            return img.n_frames - 1, int(duration)
    except Exception as e:
        print(e)
        return 0, 0
