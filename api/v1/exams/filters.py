from django_filters import rest_framework as filters

from api.v1.questions.models import StudentWrongAnswer


class WrongQuestionsExamFilter(filters.FilterSet):
    my_questions = filters.BooleanFilter(label='my_questions', field_name='my_questions')
    counts = filters.NumberFilter(label='counts', field_name='counts')

    class Meta:
        model = StudentWrongAnswer
        fields = ['my_questions', 'counts']
