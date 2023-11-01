from datetime import timedelta
from django.db import transaction
from django.conf import settings
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth import user_login_failed
from django.utils.timezone import now
from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

from api.v1.exams.models import CategoryExamStudentResult, CategoryExamStudent, StudentLastExamResult
from api.v1.levels.models import Level
from api.v1.accounts.tasks import create_objects_for_student
from api.v1.lessons.models import LessonStudent, StudentLessonViewStatistics
from api.v1.accounts.models import CustomUser
from api.v1.chapters.models import ChapterStudent
from api.v1.general.services import normalize_text
from api.v1.questions.models import StudentSavedQuestion, StudentWrongAnswer, StudentCorrectAnswer
from api.v1.accounts.services import delete_not_confirmed_accounts
from api.v1.authentications.tasks import send_confirm_link_email


@receiver(user_login_failed)
def check_user_verification(*args, **kwargs):
    email = kwargs['credentials'].get('email')
    username = kwargs['credentials'].get('username')
    email = email if email else username

    request = kwargs['request']
    password = request.POST.get('password')

    if email and password:

        try:
            user = CustomUser.objects.get(email=email, is_staff=False, is_verified=False, is_active=True)
        except CustomUser.DoesNotExist:
            return

        if not user.check_password(password):
            return

        if user.date_joined > now() - timedelta(minutes=2):
            return

        key_name = f'{email}_resend_email_verify_link'
        attempt = cache.get(key_name)
        if not attempt:
            cache.set(key_name, 1, 60 * 60 * 24)
        elif attempt >= 3:
            return
        else:
            cache.incr(key_name)

        token = default_token_generator.make_token(user)
        current_site = get_current_site(request)
        send_confirm_link_email.delay(str(user), user.pk, token, current_site.domain, user.email)


@receiver(pre_save, sender=CustomUser)
def change_fields_pre_save(instance, *args, **kwargs):
    instance.first_name, instance.last_name = normalize_text(instance.first_name, instance.last_name)
    if not instance.is_staff:
        instance.ball = instance.correct_answers * settings.TEST_BALL + instance.completed_lessons * settings.LESSON_BALL
        instance.bonus_money = round(instance.bonus_money, 1)

        level = Level.objects.filter(correct_answers__lte=instance.ball).order_by('ordering_number').last()
        gt_level = Level.objects.filter(correct_answers__gt=instance.ball).order_by('ordering_number').first()

        instance.level_id = level.ordering_number
        instance.level_percent = int(instance.ball / gt_level.correct_answers) if gt_level else 100

    if not instance.pk:
        if instance.is_staff:
            instance.user_code = instance.email
            instance.is_verified = True

        else:
            instance.user_code = instance.generate_unique_user_code


@receiver(post_save, sender=CustomUser)
def generation_objects_for_student(instance, created, *args, **kwargs):
    if created and not instance.is_staff:
        create_objects_for_student.delay(instance.pk)
        delete_not_confirmed_accounts()


@receiver(pre_delete, sender=CustomUser)
@transaction.atomic
def delete_relation_objects(instance, *args, **kwargs):
    ChapterStudent.objects.filter(student_id=instance.pk).delete()
    CategoryExamStudent.objects.filter(result__student_id=instance.pk).delete()
    CategoryExamStudentResult.objects.filter(student_id=instance.pk).delete()
    StudentLessonViewStatistics.objects.filter(student_id=instance.pk).delete()
    LessonStudent.objects.filter(student_id=instance.pk).delete()
    StudentLastExamResult.objects.filter(student_id=instance.pk).delete()
    StudentSavedQuestion.objects.filter(student_id=instance.pk).delete()
    StudentWrongAnswer.objects.filter(student_id=instance.pk).delete()
    StudentCorrectAnswer.objects.filter(student_id=instance.pk).delete()
