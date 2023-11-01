from django.utils.translation import activate

from api.v1.languages.models import Language


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = str(request.GET.get('language_id'))
        languages = Language.get_languages()
        if language in languages:
            activate(language)
        else:
            activate(languages[0])

        response = self.get_response(request)
        return response
