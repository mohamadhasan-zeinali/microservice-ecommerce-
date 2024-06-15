from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet
router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')

app_name = 'order'
urlpatterns = [
    path('api/', include(router.urls)),
]