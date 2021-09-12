import pytest
from rest_framework.exceptions import ValidationError

from ..rules import TicTacToeRules


def test_current_player_first_player():
    """Tests that first player to play is X."""
    rules = TicTacToeRules('         ')
    assert rules.current_player() == 'X'


def test_current_player_second_move():
    """Tests that second player to play is O."""
    rules = TicTacToeRules('X        ')
    assert rules.current_player() == 'O'


def test_current_player_third_move():
    """Tests that third move should be X."""
    rules = TicTacToeRules('XO       ')
    assert rules.current_player() == 'X'


def test_move_on_empty_field():
    """Tests that move works on empty places."""
    rules = TicTacToeRules('         ')
    try:
        for row in range(3):
            for column in range(3):
                rules.move(row, column)
    except Exception:
        pytest.fail('Placing a mark on empty field resulted in an exception')

    assert rules.field == 'XOXOXOXOX'


def test_move_on_filled_place():
    """Test that exception is raised on attempt to put a mark in an already
    filled place."""
    rules = TicTacToeRules('X       O')
    with pytest.raises(ValidationError):
        rules.move(2, 2)


def test_check_win():
    """Test that check_win correctly determines a winner."""
    rules = TicTacToeRules('XO OX   X')
    assert rules.check_win() == 'X'

    rules = TicTacToeRules('OX OX O X')
    assert rules.check_win() == 'O'


def test_is_finished():
    """Test is_finished method."""
    rules = TicTacToeRules('XOXOXOOX ')
    assert rules.is_finished() is False

    rules = TicTacToeRules('XOXOXOXOX')
    assert rules.is_finished() is True
