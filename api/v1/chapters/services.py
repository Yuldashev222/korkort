def chapter_image_location(instance, image):
    return f'chapters/{str(instance).replace(" ", "_")}/images/{image}'
