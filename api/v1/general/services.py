from django.conf import settings


def normalize_text(*fields) -> list:
    return [' '.join(field.split()) for field in fields]


def check_category(category_id: int) -> bool:
    return category_id in list(map(lambda item: item[0], settings.QUESTION_CATEGORIES))
