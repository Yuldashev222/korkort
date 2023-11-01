from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from api.v1.books.models import BookChapter
from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save


@receiver(post_delete, sender=BookChapter)
def delete_audio(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'audio')


@receiver(pre_save, sender=BookChapter)
def delete_audio(instance, *args, **kwargs):
    delete_object_file_pre_save(BookChapter, instance, 'audio')
