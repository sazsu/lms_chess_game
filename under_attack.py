WHITE = 1
BLACK = 2


class Knight:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'N'

    def get_color(self):
        return self.color

    def can_move(self, row1, col1):
        if not 0 <= row1 < 8 or not 0 <= col1 < 8:
            return False
        if self.row == row1 or self.col == col1:
            return False
        if abs(self.row - row1) + abs(self.col - col1) != 3:
            return False
        return True


class Bishop:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        if not 0 <= row1 < 8 or not 0 <= col1 < 8:
            return False
        if self.row == row1 or self.col == col1:
            return False
        if abs(self.row - row1) != abs(self.col - col1):
            return False
        return True

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return 'B'


class Queen:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def can_move(self, row1, col1):
        if not 0 <= row1 < 8 or not 0 <= col1 < 8:
            return False
        if (abs(self.row - row1) != abs(self.col - col1)) and (
                self.row != row1 and self.col != col1):
            return False
        return True

    def set_position(self, row1, col1):
        self.row = row1
        self.col = col1

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'


class Rook:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def char(self):
        return 'R'

    def get_color(self):
        return self.color

    def can_move(self, row, col):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if self.row != row and self.col != col:
            return False

        return True


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернет True.
        Если нет --- вернет False"""

        # if not correct_coords(row, col) or not correct_coords(row1, col1):
        if ((not 0 <= row < 8 and 0 <= col < 8) or
                (not 0 <= row1 < 8 and 0 <= col1 < 8)):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if not piece.can_move(row1, col1):
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        # self.color = opponent(self.color)
        self.color = WHITE if self.color == BLACK else BLACK
        return True

    def is_under_attack(self, row, col, color):
        for r in range(len(self.field)):
            for c in range(len(self.field)):
                piece = self.field[r][c]
                if piece and piece.get_color() == color:  # проверяем, что по координатам есть фигура, сверяем цвет
                    if piece.can_move(row, col):
                        return True
