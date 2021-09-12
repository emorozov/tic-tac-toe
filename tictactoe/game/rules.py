from typing import Literal, Union

from rest_framework.exceptions import ValidationError


Player = Literal['X', 'O']


class TicTacToeRules:
    """Implements tictactoe game rules."""
    SOLUTIONS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    def __init__(self, field: str):
        self.field = field

    def current_player(self) -> Player:
        """Determine which player plays next."""
        count_x = self.field.count('X')
        count_o = self.field.count('O')
        return 'O' if count_x > count_o else 'X'

    def move(self, row: int, column: int) -> None:
        """Puts a mark on the field at the specified position."""
        if not self.field[row * 3 + column].isspace():
            raise ValidationError('Place is already filled')

        mark = self.current_player()
        field = list(self.field)
        field[row * 3 + column] = mark
        self.field = ''.join(field)

    def check_win(self) -> Union[Player, Literal[False]]:
        """Return `X` if X won, `O` if O won, False otherwise."""
        x_won = o_won = False
        for solution in self.SOLUTIONS:
            x_won = all(self.field[pos] == 'X' for pos in solution)
            o_won = all(self.field[pos] == 'O' for pos in solution)
            if x_won or o_won:
                break

        return 'X' if x_won else 'O' if o_won else False

    def is_finished(self) -> bool:
        """Returns True if board is full."""
        return (not any(p.isspace() for p in self.field) or
                self.check_win() is not False)

    def __str__(self) -> str:
        return f'{self.field[:3]}\n{self.field[3:6]}\n{self.field[6:]}'
