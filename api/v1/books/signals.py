from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_delete, pre_save, post_save

from api.v1.books.models import BookChapter, Book
from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save


@receiver([post_save, post_delete], sender=Book)
def clear_books_cache(*args, **kwargs):
    cache.clear()


@receiver(post_delete, sender=BookChapter)
def delete_audio(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'audio')
    cache.clear()


@receiver(post_save, sender=BookChapter)
def delete_audio(instance, *args, **kwargs):
    cache.clear()


@receiver(pre_save, sender=BookChapter)
def delete_audio(instance, *args, **kwargs):
    delete_object_file_pre_save(BookChapter, instance, 'audio')
