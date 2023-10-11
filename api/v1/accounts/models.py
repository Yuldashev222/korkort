import string
import secrets

from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _, get_language
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password

from api.v1.levels.models import Level, LevelDetail
from api.v1.questions.models import Question
from api.v1.accounts.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    email = models.EmailField(_("email address"), unique=True)
    password = models.CharField(_("password"), max_length=128, validators=[validate_password])
    first_name = models.CharField(_("name"), max_length=50)
    last_name = models.CharField(_("surname"), max_length=100)

    avatar_id = models.PositiveSmallIntegerField(blank=True, null=True)
    user_code = models.CharField(max_length=400, unique=True)
    bonus_money = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    level = models.PositiveSmallIntegerField(default=0)
    auth_provider = models.CharField(max_length=100, default='-')

    completed_lessons = models.PositiveSmallIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)

    tariff_expire_date = models.DateTimeField(default=now)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['-date_joined']

    def get_level_and_gt_correct_count(self):
        level_correct_counts = Level.get_level_correct_counts()

        if not level_correct_counts:
            return '-', 1

        if self.correct_answers <= level_correct_counts[0]:
            level = LevelDetail.objects.filter(language=get_language()).first()
            if not level:
                return '-', 1

            try:
                return level.name, level_correct_counts[1]
            except IndexError:
                return level.name, 1

        for idx, cnt in enumerate(level_correct_counts):
            if self.correct_answers < cnt:
                return LevelDetail.objects.filter(language=get_language())[idx - 1], level_correct_counts[idx]
        return LevelDetail.objects.filter(language=get_language())[-1], self.correct_answers

    def __str__(self):
        return self.get_full_name()[:30]

    @property
    def generate_unique_user_code(self):
        while True:
            value = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not CustomUser.objects.filter(user_code=value).exists():
                return value

    @property
    def is_active_user(self):
        return self.is_active and self.is_verified

    @classmethod
    def user_id_exists(cls, user_code):
        return CustomUser.objects.filter(user_code=user_code, is_staff=False, is_active=True, is_verified=True).exists()
