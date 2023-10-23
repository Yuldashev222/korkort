
duplicate_rows = Question.objects.values('lesson', 'ordering_number').annotate(count=models.Count('id')).filter(count__gt=1)
duplicate_rows = Question.objects.filter(lesson__in=duplicate_rows.values('lesson'), ordering_number__in=duplicate_rows.values('ordering_number'))
