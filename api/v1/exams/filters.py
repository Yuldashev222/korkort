from django_filters import rest_framework as filters

from api.v1.questions.models import StudentWrongAnswer, StudentSavedQuestion


class WrongQuestionsExamFilter(filters.FilterSet):
    my_questions = filters.BooleanFilter(label='my_questions', field_name='my_questions')
    counts = filters.NumberFilter(label='counts', field_name='counts')
    difficulty_level = filters.NumberFilter(label='difficulty_level', field_name='difficulty_level')

    class Meta:
        model = StudentWrongAnswer
        fields = ['my_questions', 'counts']


class SavedQuestionsExamFilter(WrongQuestionsExamFilter):
    class Meta(WrongQuestionsExamFilter.Meta):
        model = StudentSavedQuestion
