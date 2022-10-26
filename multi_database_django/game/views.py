from rest_framework import viewsets

from .models import Game
from .serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.using('default').all()

