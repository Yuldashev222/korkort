from django.utils.translation import activate

from api.v1.languages.models import Language


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = str(request.GET.get('language_id'))
        languages = Language.get_languages()
        try:
            default_language = str(languages[0])
        except IndexError:
            default_language = 1
        try:
            language = int(language)
        except ValueError:
            activate(default_language)
        else:
            if language in languages:
                activate(str(language))
            else:
                activate(default_language)

        response = self.get_response(request)
        return response
