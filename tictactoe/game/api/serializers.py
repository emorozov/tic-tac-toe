from rest_framework import serializers

from ..models import Game, Scoreboard


class GameSerializer(serializers.ModelSerializer):
    is_finished = serializers.ReadOnlyField()
    victorious_player = serializers.ReadOnlyField()

    class Meta:
        model = Game
        fields = ['id', 'player_x', 'player_o', 'field', 'is_finished',
                  'victorious_player']


class MoveSerializer(serializers.Serializer):
    row = serializers.IntegerField(min_value=0, max_value=2)
    column = serializers.IntegerField(min_value=0, max_value=2)


class ScoreboardSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    score = serializers.ReadOnlyField()

    class Meta:
        model = Scoreboard
        fields = ['username', 'score']
