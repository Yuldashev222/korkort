from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static

from .yasg import schema_view

urlpatterns = [
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/v1/payments/', include('api.v1.payments.urls')),
    path('api/v1/auth/', include('api.v1.authentications.urls')),
    path('api/v1/tariffs/', include('api.v1.tariffs.urls')),
    path('api/v1/accounts/', include('api.v1.accounts.urls')),

    path("__debug__/", include("debug_toolbar.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('asdasdasd/', include('rest_framework.urls'))]
