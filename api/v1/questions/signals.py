from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from api.v1.exams.models import CategoryExamStudentResult
from api.v1.general.utils import delete_object_file_pre_save, delete_object_file_post_delete
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question, Category


@receiver(post_delete, sender=Question)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')
    delete_object_file_post_delete(instance, 'gif')
    Question.set_redis()


@receiver(pre_save, sender=Question)
def delete_image(instance, *args, **kwargs):
    try:
        delete_object_file_pre_save(Question, instance, 'image')
        delete_object_file_pre_save(Question, instance, 'gif')
    except Question.DoesNotExist:
        pass


@receiver(post_save, sender=Question)
def update_question_count(*args, **kwargs):
    Question.set_redis()


@receiver(pre_save, sender=Category)
def delete_image(instance, *args, **kwargs):
    try:
        delete_object_file_pre_save(Category, instance, 'image')
    except Category.DoesNotExist:
        pass


@receiver(post_delete, sender=Category)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')


@receiver(post_save, sender=Category)
def create_student_exams(instance, created, *args, **kwargs):
    if created:
        objs = [
            CategoryExamStudentResult(category=instance, student=student)
            for student in CustomUser.objects.filter(is_staff=False)
        ]
        CategoryExamStudentResult.objects.bulk_create(objs)
