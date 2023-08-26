def normalize_text(*fields):
    return [' '.join(field.split()) for field in fields]
