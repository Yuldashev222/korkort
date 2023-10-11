from django.core.management.base import BaseCommand
from api.v1.languages.models import Language
from api.v1.levels.models import Level, LevelDetail

LEVEL_CORRECT_COUNTS = [0, 50, 150, 300, 500, 750, 1150, 1650, 2350, 3200]
LEVEL_NAMES_SWE = [
    'Nyckelknippe',
    'Startmotorn',
    'Asfaltsrookie',
    'Kopplingskung',
    'Vägkapten',
    'Kurvmästare',
    'Gasguru',
    'Fartfantast',
    'Bilboss',
    'Körkortskung'
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for idx, i in enumerate(LEVEL_CORRECT_COUNTS):
            level = Level.objects.create(correct_answers=i, ordering_number=idx + 1)
            for language in Language.objects.all():
                LevelDetail.objects.create(level=level, language=language,
                                           name=f'{language.language_id}_{LEVEL_NAMES_SWE[idx]}')

        Level.set_redis()
