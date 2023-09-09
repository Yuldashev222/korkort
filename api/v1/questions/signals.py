from django.dispatch import receiver
from django.db.models import Count
from django.db.models.signals import post_save, post_delete, pre_save

from api.v1.exams.models import CategoryExamStudent
from api.v1.general.utils import delete_object_file_pre_save, delete_object_file_post_delete
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question, QuestionStudentLastResult, Category


@receiver(post_delete, sender=Question)
def delete_image(instance, *args, **kwargs):
    Question.set_redis()
    delete_object_file_post_delete(instance, 'image')
    delete_object_file_post_delete(instance, 'video')


@receiver(pre_save, sender=Question)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(Question, instance, 'image')
    delete_object_file_pre_save(Question, instance, 'video')


@receiver(post_delete, sender=Category)
def delete_image(instance, *args, **kwargs):
    delete_object_file_post_delete(instance, 'image')


@receiver(pre_save, sender=Category)
def delete_image(instance, *args, **kwargs):
    delete_object_file_pre_save(Category, instance, 'image')


@receiver(post_save, sender=Question)
def update_question_count(*args, **kwargs):
    Question.set_redis()


@receiver(post_save, sender=QuestionStudentLastResult)
def delete_the_excess(instance, *args, **kwargs):
    if instance.student:
        expire_objs = QuestionStudentLastResult.objects.filter(student=instance.student
                                                               ).values_list('id', flat=True)[10:]
        QuestionStudentLastResult.objects.filter(student=instance.student, id__in=expire_objs).delete()

        data = QuestionStudentLastResult.objects.filter(student=instance.student).aggregate(
            questions=Count('questions'), answers=Count('wrong_answers'))
        all_questions = data['questions']
        all_correct_answers = all_questions - data['answers']
        instance.student.last_exams_result = int(all_correct_answers / all_questions * 100)
        instance.student.save()


@receiver(post_save, sender=Category)
def create_student_exams(instance, created, *args, **kwargs):
    if created:
        objs = [
            CategoryExamStudent(category=instance, student=student)
            for student in CustomUser.objects.filter(is_staff=False)
        ]
        CategoryExamStudent.objects.bulk_create(objs)
