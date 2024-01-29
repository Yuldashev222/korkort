from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve

from .yasg import schema_view


@login_required
def custom_serve(*args, **kwargs):
    return serve(*args, **kwargs)


def custom_static(*args, **kwargs):
    return static(view=custom_serve, *args, **kwargs)


urlpatterns = [

    path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/v1/general/', include('api.v1.general.urls')),
    path('api/v1/payments/', include('api.v1.payments.urls')),
    path('api/v1/auth/', include('api.v1.authentications.urls')),
    path('api/v1/tariffs/', include('api.v1.tariffs.urls')),
    path('api/v1/accounts/', include('api.v1.accounts.urls')),
    path('api/v1/lessons/', include('api.v1.lessons.urls')),
    path('api/v1/chapters/', include('api.v1.chapters.urls')),
    path('api/v1/questions/', include('api.v1.questions.urls')),
    path('api/v1/exams/', include('api.v1.exams.urls')),
    path('api/v1/swish/', include('api.v1.swish.urls')),
    path('api/v1/books/', include('api.v1.books.urls')),
    path('api/v1/todos/', include('api.v1.todos.urls')),
    path('api/v1/reports/', include('api.v1.reports.urls')),
    path('api/v1/notifications/', include('api.v1.notifications.urls')),

    path("__debug__/", include("debug_toolbar.urls"))

]

urlpatterns += [path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file")]
urlpatterns += custom_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('asdasdasd/', include('rest_framework.urls'))]  # last
