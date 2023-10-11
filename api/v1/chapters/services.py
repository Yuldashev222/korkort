def chapter_image_location(instance, image):
    normalize_chapter_name = str(instance).replace(" ", "_")
    return f'chapters/{normalize_chapter_name}/images/{image}'
