def m3u8_file_location(lesson_detail, m3u8_file):
    return (f'chapters/{lesson_detail.lesson.chapter_id}/lessons/{lesson_detail.lesson_id}/'
            f'videos/{lesson_detail.language_id}/hls/{m3u8_file}')
