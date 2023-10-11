from uuid import uuid4
from django.core.management.base import BaseCommand

from api.v1.general.enums import title, desc
from api.v1.lessons.models import Lesson
from api.v1.languages.models import Language
from api.v1.questions.models import Category, Question, Variant, CategoryDetail, QuestionDetail


def create_categories():
    for i in range(40):
        obj = Category.objects.create(image='chapters/1:_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png',
                                      ordering_number=i + 1)
        for language in Language.objects.all():
            CategoryDetail.objects.create(category=obj, language=language, name=title)


def create_questions(self):
    categories = Category.objects.all()
    lessons = Lesson.objects.order_by('-id')
    lst = []
    for lesson in lessons:
        self.stdout.write(str(lesson.id))

        for index, category in enumerate(categories, 1):
            if index > 7:
                difficulty_level = Question.DIFFICULTY_LEVEL[2][0]
            elif index % 2 == 0:
                difficulty_level = Question.DIFFICULTY_LEVEL[0][0]
            else:
                difficulty_level = Question.DIFFICULTY_LEVEL[1][0]

            obj = Question.objects.create(difficulty_level=difficulty_level, lesson=lesson, category=category,
                                          ordering_number=index, gif='a.gif',
                                          image='chapters/1:_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')

            for language in Language.objects.all():
                lst.append(QuestionDetail(question=obj, language=language, text=str(uuid4()), answer=desc))

        for index, category in enumerate(categories, 1):
            if index > 7:
                difficulty_level = Question.DIFFICULTY_LEVEL[2][0]
            elif index % 2 == 0:
                difficulty_level = Question.DIFFICULTY_LEVEL[0][0]
            else:
                difficulty_level = Question.DIFFICULTY_LEVEL[1][0]

            obj = Question.objects.create(category=category, ordering_number=100000, difficulty_level=difficulty_level,
                                          gif='a.gif',
                                          image='chapters/1:_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')

            for language in Language.objects.all():
                lst.append(QuestionDetail(question=obj, language=language, text=str(uuid4()), answer=desc))

    QuestionDetail.objects.bulk_create(lst)
    Question.set_redis()


def create_variants(self):
    objs = []
    questions = Question.objects.order_by('-id')
    for question in questions:
        self.stdout.write(str(question.id))
        for i in range(4):
            for language in Language.objects.all():
                objs.append(Variant(question=question, language=language, is_correct=i == 2, text=str(uuid4())))
    Variant.objects.bulk_create(objs)


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_categories()
        create_questions(self)
        create_variants(self)
