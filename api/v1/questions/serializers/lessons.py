from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.balls.models import TestBall
from api.v1.lessons.models import LessonStudent
from api.v1.questions.tasks import update_student_wrong_answers_in_lesson_exam
from api.v1.questions.models import Question, QuestionStudentLastResult
from api.v1.questions.serializers.questions import QuestionAnswerSerializer


class LessonAnswerSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        lesson_id = data['lesson_id']
        student = self.context['request'].user

        try:
            lesson_student = LessonStudent.objects.select_related('lesson').get(id=lesson_id, student=student)
            lesson = lesson_student.lesson
        except LessonStudent.DoesNotExist:
            raise ValidationError({'lesson_id': 'not found.'})

        question_ids = list(set(question['pk'] for question in data['questions']))

        for pk in question_ids:
            if not Question.is_correct_question_id(question_id=pk):
                raise ValidationError({'pk': 'not found'})

        test_ball = TestBall.get_ball()

        if not test_ball:
            return {}

        wrong_answers_cnt = len(question_ids)
        correct_question_ids = list(lesson.question_set.exclude(id__in=question_ids).values_list('pk', flat=True))
        lesson_all_questions_cnt = wrong_answers_cnt + len(correct_question_ids)
        QuestionStudentLastResult.objects.create(wrong_answers=wrong_answers_cnt, questions=lesson_all_questions_cnt,
                                                 student=student)
        if wrong_answers_cnt == 0:
            lesson_student.is_completed = True

        lesson_student.ball = (lesson_all_questions_cnt - wrong_answers_cnt) * test_ball
        lesson_student.save()

        update_student_wrong_answers_in_lesson_exam.delay(correct_question_ids=correct_question_ids,
                                                          wrong_question_ids=question_ids,
                                                          lesson_id=lesson.id, student_id=student.id)

        return data
