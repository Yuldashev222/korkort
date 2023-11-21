from datetime import timedelta
from django.utils.timezone import now
from django.utils.translation import get_language

from api.v1.accounts.models import CustomUser
from api.v1.levels.models import LevelDetail


def delete_not_confirmed_accounts():
    CustomUser.objects.filter(date_joined__lte=now() - timedelta(days=1), is_staff=False, is_verified=False).delete()


def get_student_level(student, old_level_id):
    level = {}
    if old_level_id != student.level_id:
        level = {
            'pk': student.level_id,
            'percent': student.level_percent
        }
        try:
            obj = LevelDetail.objects.get(language_id=get_language(), level__ordering_number=student.level_id)
        except LevelDetail.DoesNotExist:
            level['name'] = '-'
        else:
            level['name'] = obj.name
    return level
