from django.urls import path
from api.v1.notifications.views import NotificationAPIView

urlpatterns = [
    path('', NotificationAPIView.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', NotificationAPIView.as_view({'get': 'retrieve',
                                                   'put': 'update',
                                                   'patch': 'partial_update',
                                                   'delete': 'destroy'
                                                   })),
]
