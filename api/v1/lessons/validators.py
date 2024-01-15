from zipfile import ZipFile

from django.core.exceptions import ValidationError

url = "/home/oybek/Videos/21886880cef1406e976619c5dc97b9fd.zip"


def validate_m3u8_zip_file(m3u8_zip_file_url):
    with ZipFile(m3u8_zip_file_url) as z:
        m3u8_file_exists = False
        for i in z.filelist:
            filename = i.filename
            ts_file, m3u8_file = filename.endswith('.ts'), filename.endswith('.m3u8')

            if not (ts_file or m3u8_file):
                raise ValidationError("format error")

            elif m3u8_file:
                if m3u8_file_exists:
                    raise ValidationError("m3u8 more one")
                m3u8_file_exists = True
