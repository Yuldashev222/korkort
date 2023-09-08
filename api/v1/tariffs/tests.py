import re
from datetime import datetime
from collections import OrderedDict
from elasticsearch_dsl import Q
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .tasks import create_search_detail_obj
from .enums import InformCountry, InformRegion
from .models import FileDetail
from .documents import FileDetailDocument
from .serializers import FileDetailDocumentSerializer, FileDetailDocumentAuthSerializer


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        count = self.page.paginator.count
        return count
        search_text = self.request.query_params.get('search', '').strip()
        if bool(search_text):
            create_search_detail_obj.delay(
                search_text=search_text,
                files_cnt=count,
                forwarded=self.request.META.get('HTTP_X_FORWARDED_FOR'),
                real=self.request.META.get('HTTP_X_REAL_IP'),
                remote=self.request.META.get('REMOTE_ADDR')
            )
        return Response(OrderedDict([
            ('count', count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class SearchFilesView(ListAPIView):
    pagination_class = CustomPageNumberPagination
    document_class = FileDetailDocument
    queryset = FileDetail.objects.all()
    permission_classes = ()

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return FileDetailDocumentSerializer
        return FileDetailDocumentAuthSerializer

    @staticmethod
    def all_q_expression(query):
        a = query
        b = query.split()
        b.reverse()
        r_query = ' '.join(b)
        add_query = ' '.join(r_query)
        q = Q('bool',
              must=[
                  Q('regexp', text=f'{a}.*') |
                  Q('regexp', text=f'{add_query}.*') |
                  Q('regexp', text=f'{r_query}.*')
              ]) | Q('bool',
                     should=[
                         Q('match_phrase', text={'query': f'{a}.*', 'slop': 10}) |
                         Q('match_phrase', text={'query': f'{r_query}.*', 'slop': 10})
                     ])
        return q

    @staticmethod
    def ignore_q_expression(query):
        return Q('bool',
                 must_not=[
                     Q('regexp', text=f'{query}.*') |
                     Q('regexp', text=f'{" ".join(query)}.*')
                 ])

    @staticmethod
    def exact_q_expression(query):
        return Q(
            'bool',
            should=[
                Q('match_phrase', text=query) |
                Q('match_phrase', text=' '.join(query))
            ],
            minimum_should_match=1
        )

    @staticmethod
    def filter_q_expression(dct):
        return Q('term', **dct)

    @staticmethod
    def date_q_expression(year):
        start_date = datetime(year=year, month=1, day=1)
        end_date = datetime(year=year, month=12, day=31)
        return Q(
            'range',
            file_date={'gte': start_date, 'lte': end_date}
        )

    def get(self, request, *args, **kwargs):
        search_query = str(request.query_params.get('search', '')).strip()
        ordering_query = str(request.query_params.get('ordering', '')).strip()
        filter_date_query = str(request.query_params.get('file_date', '')).strip()

        search = self.document_class.search().sort({'_id': {'order': 'desc'}})
        if bool(filter_date_query) and len(filter_date_query) == 4 and filter_date_query.isdigit():
            year = int(filter_date_query)
            try:
                search = search.query(self.date_q_expression(year))
            except:
                pass

        filter_organ_query = str(request.query_params.get('organ', '')).strip()
        if bool(filter_organ_query) and len(filter_organ_query) == 1 and filter_organ_query in 'sf':
            search = search.query(self.filter_q_expression({'organ': filter_organ_query}))

        filter_country_query = str(request.query_params.get('country', '')).strip()
        if bool(filter_country_query) and filter_country_query in InformCountry.keys():
            search = search.query(self.filter_q_expression({'country': filter_country_query}))

        filter_region_query = str(request.query_params.get('region', '')).strip()
        if bool(filter_region_query) and filter_region_query in InformRegion.keys():
            search = search.query(self.filter_q_expression({'region': filter_region_query}))

        bol = bool(search_query)
        if bol:
            search_query = ' '.join(search_query.split()).lower()
            s_copy = search_query

            # required text expression
            required_pattern = r'".{,}"'
            required_text = re.search(required_pattern, search_query)
            if bool(required_text):
                required_text = required_text.group()
                required_text = required_text[1:required_text.index('"', 1)]
            # ----------------

            # ignore text expression
            ignore_texts = list(filter(lambda el: el[0] == '-', str(' ' + search_query + ' ').split()))
            if bool(ignore_texts):
                for i in ignore_texts:
                    q_text = self.ignore_q_expression(i.replace('-', ''))
                    search = search.query(q_text)
                    if bool(required_text):
                        if i not in required_text:
                            search_query = search_query.replace(i, '')
                        else:
                            asd = search_query.replace(required_text, '')
                            if i in asd:
                                dsa = search_query.split()
                                dsa.reverse()
                                cnt = asd.count(i)
                                while cnt > 0:
                                    dsa.remove(i)
                                    cnt -= 1
                                dsa.reverse()
                                search_query = ' '.join(dsa).strip()
                    else:
                        search_query = search_query.replace(i, '')
            # ---------------------

            # all expression
            search_query = search_query.replace('"', '')
            if bool(search_query.strip()):
                q = self.all_q_expression(search_query.strip())
                search = search.query(q).sort({"_score": {"order": "desc"}})
            # -------------

            # required text expression
            if bool(required_text):
                q = self.exact_q_expression(required_text)
                search = search.query(q).sort({"_score": {"order": "desc"}})
            # -----------------------
            search = search.highlight(
                'text', fragment_size=130, pre_tags='<mark>', post_tags='</mark>', max_analyzed_offset=500000
            )

        if bool(ordering_query) and ordering_query in ['-file_date', 'file_date']:
            if ordering_query.startswith('-'):
                search = search.sort('-file_date')
            else:
                search = search.sort('file_date')

        page = request.query_params.get('page', 1)
        try:
            response = search[(int(page) - 1) * 10:].execute()
        except Exception as e:
            print(e)
            response = search.execute()
        serializer = self.get_serializer_class()
        serializer = serializer(response, many=True, context={'request': request, 'bol': bol})
        self.paginate_queryset(search)
        count = self.get_paginated_response(search)
        if bol:
            create_search_detail_obj.delay(
                search_text=s_copy,
                files_cnt=count,
                forwarded=request.META.get('HTTP_X_FORWARDED_FOR'),
                real=request.META.get('HTTP_X_REAL_IP'),
                remote=request.META.get('REMOTE_ADDR')
            )
        return Response(OrderedDict([
            ('count', count),
            ('results', serializer.data)
        ]))
