from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GameViewSet, ScoreboardView


router = DefaultRouter()
router.register('', GameViewSet, basename='game')

urlpatterns = [
    path('hiscore/', ScoreboardView.as_view(), name='hiscore'),
] + router.urls
