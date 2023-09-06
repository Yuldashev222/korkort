from django.utils.translation import activate
from django.conf import settings


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.GET.get('language')

        if language and language in settings.CUSTOM_LANGUAGES:
            activate(language)
        else:
            activate(settings.CUSTOM_LANGUAGES[0])

        response = self.get_response(request)
        return response
