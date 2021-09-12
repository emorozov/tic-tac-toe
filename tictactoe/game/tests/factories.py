import factory
from django.contrib.auth.models import User

from tictactoe.game.models import Game


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    email = factory.Sequence(lambda num: f'email-{num}@test.dev')
    username = factory.Sequence(lambda num: f'username-{num}')
    password = factory.PostGenerationMethodCall('set_password', '123456')

    class Meta:
        model = User


class GameFactory(factory.django.DjangoModelFactory):
    """Game factory."""

    player_x = factory.SubFactory(UserFactory)
    player_o = factory.SubFactory(UserFactory)

    class Meta:
        model = Game
