import uuid

from django.db import models
from django.contrib.auth.models import User

from .rules import TicTacToeRules


class Game(models.Model):
    """Stores information about players and game field."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    player_x = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                                 related_name='x_games')
    player_o = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                                 related_name='o_games')
    field = models.CharField(max_length=9, null=False, default=' ' * 9)

    def __str__(self):
        return self.field

    def is_finished(self):
        return TicTacToeRules(self.field).is_finished()

    def victorious_player(self):
        return TicTacToeRules(self.field).check_win()


class Scoreboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)

    def __str__(self):
        return str(self.user)
