from PIL import Image


def get_last_frame_number(gif_path):
    try:
        with Image.open(gif_path) as img:
            return img.n_frames - 1
    except Exception as e:
        return None


# Provide the path to your GIF file
gif_path = '../../../media/giphy (1).gif'
last_frame_number = get_last_frame_number(gif_path)

if last_frame_number is not None:
    print(f"Last frame number: {last_frame_number}")
else:
    print("Failed to retrieve the last frame number.")
