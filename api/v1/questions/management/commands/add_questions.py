from uuid import uuid4

from django.core.management.base import BaseCommand

from api.v1.lessons.models import Lesson
from api.v1.questions.models import Category, Question, Variant


def create_categories():
    for i in range(10):
        Category.objects.create(name_swe=str(uuid4()),
                                name_en=str(uuid4()),
                                name_e_swe=str(uuid4()),
                                image='discounts/images/IMG.png')


def create_lesson_questions(self):
    categories = Category.objects.all()
    lessons = Lesson.objects.order_by('-id')
    objs1 = []
    objs2 = []
    for lesson in lessons:
        self.stdout.write(str(lesson.id))
        for index, category in enumerate(categories, 1):
            if index > 7:
                difficulty_level = Question.DIFFICULTY_LEVEL[2][0]
            else:
                difficulty_level = Question.DIFFICULTY_LEVEL[0][0] if index % 2 == 0 else Question.DIFFICULTY_LEVEL[1][
                    0]
            objs1.append(Question(lesson=lesson,
                                  category=category,
                                  for_lesson=True,
                                  ordering_number=index,
                                  difficulty_level=difficulty_level,
                                  answer=f'{str(uuid4())}' * 3,
                                  text_swe=f'{str(uuid4())}' * 2,
                                  text_en=f'{str(uuid4())}' * 3,
                                  text_e_swe=f'{str(uuid4())}' * 4,
                                  gif='chapters/4:%20askjdbkjas%20bdkajs%20bdkja%20bsa/lessons/10:%20askjdbkjas%20bdkajs%20bdkja%20bsaaskjdbkjas%20bdkajs%20bdkja%20bsa/videos/a.mp4',
                                  image='discounts/images/IMG.png'
                                  )
                         )

        for index, category in enumerate(categories, 1):
            if index > 7:
                difficulty_level = Question.DIFFICULTY_LEVEL[2][0]
            else:
                difficulty_level = Question.DIFFICULTY_LEVEL[0][0] if index % 2 == 0 else \
                    Question.DIFFICULTY_LEVEL[1][0]
            objs2.append(Question(lesson=lesson,
                                  category=category,
                                  for_lesson=False,
                                  ordering_number=None,
                                  difficulty_level=difficulty_level,
                                  answer=f'{str(uuid4())}' * 3,
                                  text_swe=f'{str(uuid4())}' * 2,
                                  text_en=f'{str(uuid4())}' * 3,
                                  text_e_swe=f'{str(uuid4())}' * 4,
                                  gif='chapters/1%3A%20836c4b38-fe8e-4ef2-9a9c-bab/lessons/1%3A%20614101a6-4c87-4dbc-9629-23a/videos/a.mp4',
                                  image='discounts/images/IMG.png'
                                  )
                         )
    Question.objects.bulk_create(objs1)
    Question.objects.bulk_create(objs2)
    Question.set_redis()


def create_variants(self):
    objs = []
    questions = Question.objects.order_by('-id')
    for question in questions:
        self.stdout.write(str(question.id))
        for i in range(5):
            objs.append(Variant(question=question,
                                is_correct=i == 3,
                                text_en=f'{uuid4()}',
                                text_swe=f'{uuid4()}',
                                text_e_swe=f'{uuid4()}'))

    Variant.objects.bulk_create(objs)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_categories()
        create_lesson_questions(self)
        create_variants(self)
