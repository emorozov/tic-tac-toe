import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from tictactoe.game.models import Game, Scoreboard
from .factories import GameFactory, UserFactory


@pytest.mark.django_db
def test_create_game(client: APIClient):
    """Test game creation."""
    user = UserFactory()
    client.force_authenticate(user)
    response = client.post(reverse('game-list'))
    assert response.status_code == 201
    game = Game.objects.get()
    assert response.json() == {
        'id': str(game.pk),
        'field': '         ',
        'player_x': user.pk,
        'player_o': None,
        'is_finished': False,
        'victorious_player': False
    }


@pytest.mark.django_db
def test_create_game_unauthenticated(client: APIClient):
    """Test that only authenticated users can create a game."""
    response = client.post(reverse('game-list'))
    assert response.status_code == 401


@pytest.mark.django_db
def test_join_game(client: APIClient):
    """Test joining a game."""
    user_x = UserFactory()
    game = Game.objects.create(player_x=user_x)

    user_o = UserFactory()
    client.force_authenticate(user_o)
    response = client.post(reverse('game-join', args=[game.pk]))
    assert response.status_code == 200
    assert response.json() == {
        'id': str(game.pk),
        'field': '         ',
        'player_x': user_x.pk,
        'player_o': user_o.pk,
        'is_finished': False,
        'victorious_player': False
    }


@pytest.mark.django_db
def test_valid_move(client: APIClient):
    """Test making a valid move."""
    game = GameFactory()
    client.force_authenticate(game.player_x)
    response = client.post(reverse('game-move', args=[game.pk]),
                           data={'row': 0, 'column': 0})
    assert response.status_code == 200
    assert response.json() == {
        'id': str(game.pk),
        'field': 'X        ',
        'player_x': game.player_x.pk,
        'player_o': game.player_o.pk,
        'is_finished': False,
        'victorious_player': False
    }


@pytest.mark.django_db
def test_invalid_move_filled_place(client: APIClient):
    """Test marking already filled place."""
    game = GameFactory(field='X        ')
    client.force_authenticate(game.player_o)
    response = client.post(reverse('game-move', args=[game.pk]),
                           data={'row': 0, 'column': 0})
    assert response.status_code == 400
    assert response.json() == ['Place is already filled']


@pytest.mark.django_db
def test_invalid_move_wrong_turn(client: APIClient):
    """Test making two turns in a row is not accepted."""
    game = GameFactory()
    client.force_authenticate(game.player_x)
    response = client.post(reverse('game-move', args=[game.pk]),
                           data={'row': 0, 'column': 0})
    assert response.status_code == 200
    response = client.post(reverse('game-move', args=[game.pk]),
                           data={'row': 0, 'column': 1})
    assert response.status_code == 400
    assert response.json() == ['It is not your turn']


@pytest.mark.django_db
def test_winning_a_game(client: APIClient):
    """Test winning condition."""
    game = GameFactory(field='XOOXOX   ')
    client.force_authenticate(game.player_x)
    response = client.post(reverse('game-move', args=[game.pk]),
                           data={'row': 2, 'column': 0})
    assert response.status_code == 200
    assert response.json() == {
        'id': str(game.pk),
        'field': 'XOOXOXX  ',
        'player_x': game.player_x.pk,
        'player_o': game.player_o.pk,
        'is_finished': True,
        'victorious_player': 'X'
    }

    score = Scoreboard.objects.get()
    assert score.user == game.player_x
    assert score.games.first() == game


@pytest.mark.django_db
def test_scoreboard(client: APIClient):
    """Test scoreboard view."""
    player_x = UserFactory()
    player_o = UserFactory()
    game_1 = GameFactory(player_x=player_x, player_o=player_o)
    game_2 = GameFactory(player_x=player_x, player_o=player_o)
    game_3 = GameFactory(player_x=player_x, player_o=player_o)
    x_score = Scoreboard.objects.create(user=player_x)
    x_score.games.set([game_1, game_2])
    o_score = Scoreboard.objects.create(user=player_o)
    o_score.games.set([game_3])

    response = client.get(reverse('hiscore'))
    assert response.status_code == 200
    assert response.json() == [
        {'username': player_x.username, 'score': 2},
        {'username': player_o.username, 'score': 1},
    ]
