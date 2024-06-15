from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
router = DefaultRouter()

router.register('products', ProductViewSet, basename='products')

app_name = 'product'
urlpatterns =[
    path('api/', include(router.urls)),
]