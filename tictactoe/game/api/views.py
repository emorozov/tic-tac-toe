from django.db.models import Count
from django.db.transaction import atomic
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import Game, Scoreboard
from ..rules import TicTacToeRules
from .serializers import GameSerializer, MoveSerializer, ScoreboardSerializer


class GameViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=None)
    def create(self, request, *args, **kwargs):
        """Creates a new game."""
        game = Game.objects.create(player_x=request.user)
        serializer = self.get_serializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(request=None)
    @action(detail=True, methods=['post'])
    @atomic
    def join(self, request, pk=None):
        """Adds second player to the game."""
        game: Game = self.get_object()
        if game.player_o:
            raise ValidationError('Second player already joined the game')

        game.player_o = request.user
        game.save(update_fields=['player_o'])
        serializer = self.get_serializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=MoveSerializer)
    @action(detail=True, methods=['post'])
    @atomic
    def move(self, request, pk=None):
        game: Game = self.get_object()
        if not (game.player_x and game.player_o):
            raise ValidationError('Both players must be present')

        serializer = MoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rules = TicTacToeRules(game.field)
        if rules.is_finished():
            raise ValidationError('Game has already finished')

        player = rules.current_player()
        correct_player = (
            (request.user == game.player_x and player == 'X') or
            (request.user == game.player_o and player == 'O')
        )
        if not correct_player:
            raise ValidationError('It is not your turn')

        rules.move(serializer.validated_data['row'],
                   serializer.validated_data['column'])
        game.field = rules.field
        game.save(update_fields=['field'])

        victorious_player = rules.check_win()
        if victorious_player == 'X':
            board, _ = Scoreboard.objects.get_or_create(user=game.player_x)
            board.games.add(game)
        elif victorious_player == 'O':
            board, _ = Scoreboard.objects.get_or_create(user=game.player_o)
            board.games.add(game)

        game_serializer = self.get_serializer(game)
        return Response(game_serializer.data, status=status.HTTP_200_OK)


class ScoreboardView(generics.ListAPIView):
    queryset = Scoreboard.objects.annotate(
        score=Count('games')).select_related('user').order_by('-score')
    serializer_class = ScoreboardSerializer
