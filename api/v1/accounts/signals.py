from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

from api.v1.accounts.tasks import create_objects_for_student
from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import ChapterStudent
from api.v1.exams.models import CategoryExamStudentResult, CategoryExamStudent
from api.v1.lessons.models import LessonStudent, StudentLessonViewStatistics
from api.v1.questions.models import QuestionStudentLastResult, StudentSavedQuestion, StudentWrongAnswer, \
    StudentCorrectAnswer


@receiver(pre_save, sender=CustomUser)
def change_fields_pre_save(instance, *args, **kwargs):
    if not instance.pk:
        if instance.is_staff:
            instance.user_code = instance.email
            instance.is_verified = True

        else:
            instance.user_code = instance.generate_unique_user_code


@receiver(post_save, sender=CustomUser)
def generation_objects_for_student(instance, created, *args, **kwargs):
    if created and not instance.is_staff:
        create_objects_for_student.delay(instance.id)


@receiver(pre_delete, sender=CustomUser)
@transaction.atomic
def delete_relation_objects(instance, *args, **kwargs):
    ChapterStudent.objects.filter(student=instance).delete()
    CategoryExamStudent.objects.filter(result__student=instance).delete()
    CategoryExamStudentResult.objects.filter(student=instance).delete()
    StudentLessonViewStatistics.objects.filter(student=instance).delete()
    LessonStudent.objects.filter(student=instance).delete()
    QuestionStudentLastResult.objects.filter(student=instance).delete()
    StudentSavedQuestion.objects.filter(student=instance).delete()
    StudentWrongAnswer.objects.filter(student=instance).delete()
    StudentCorrectAnswer.objects.filter(student=instance).delete()
