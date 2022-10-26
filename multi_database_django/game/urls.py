from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet


router = DefaultRouter()
router.register('game', GameViewSet)


urlpatterns = [
    path('', include(router.urls)),
]