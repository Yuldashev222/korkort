import os
import shutil
from zipfile import ZipFile

from django.conf import settings


def m3u8_zip_file_location(lesson_detail, m3u8_zip_file):
    return (f'chapters/{lesson_detail.lesson.chapter_id}/lessons/{lesson_detail.lesson_id}/'
            f'videos/{lesson_detail.language_id}/zip_files/{m3u8_zip_file}')


def get_m3u8_directory_location(lesson_detail):
    return os.path.join(settings.MEDIA_ROOT,
                        f'chapters/{lesson_detail.lesson.chapter_id}/lessons/{lesson_detail.lesson_id}/videos/{lesson_detail.language_id}/hls/')


def extract_m3u8_zip_file(lesson_detail):
    with ZipFile(lesson_detail.m3u8_zip.path, 'r') as z:
        extract_location = get_m3u8_directory_location(lesson_detail=lesson_detail)
        try:
            os.makedirs(extract_location)
        except FileExistsError:
            shutil.rmtree(extract_location)
            os.makedirs(extract_location)

        z.extractall(path=extract_location)
    os.remove(lesson_detail.m3u8_zip.path)
