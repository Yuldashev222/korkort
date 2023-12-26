from django.dispatch import receiver
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, pre_save

from api.v1.general.utils import delete_object_file_pre_save, delete_object_file_post_delete
from api.v1.questions.models import Question, QuestionDetail


@receiver(post_delete, sender=Question)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')
    delete_object_file_post_delete(instance, 'video')
    cache.clear()
    Question.set_redis()


@receiver(pre_save, sender=Question)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(Question, instance, 'image')
    delete_object_file_pre_save(Question, instance, 'video')


@receiver(post_save, sender=Question)
def update_question_count(*args, **kwargs):
    cache.clear()
    Question.set_redis()


@receiver([post_save, post_delete], sender=QuestionDetail)
def update_question_count(*args, **kwargs):
    cache.clear()
