from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

from api.v1.general.utils import delete_object_file_post_delete, delete_object_file_pre_save
from api.v1.chapters.models import Chapter


@receiver(post_delete, sender=Chapter)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')


@receiver(pre_save, sender=Chapter)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(Chapter, instance, 'image')
