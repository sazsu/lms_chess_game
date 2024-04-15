class Pawn:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Rook:
    def __init__(self, color):
        self.color = color
        self.was_moved = False

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку,
        # которая не лежит в том же ряду или столбце клеток.
        if row != row1 and col != col1:
            return False

        if col == col1:  # вертикальная проверка
            step = 1 if row1 >= row else -1
            for r in range(row + step, row1 + step, step):
                # Если на пути по вертикали есть фигура
                if board.get_piece(r, col) is not None:
                    return False

        elif row == row1:  # горизонтальная проверка
            step = 1 if col1 >= col else -1
            for c in range(col + step, col1 + step, step):
                # Если на пути по горизонтали есть фигура
                if board.get_piece(row, c) is not None:
                    return False
        # путь свободен
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    def __init__(self, color):
        self.color = color

    def char(self):
        return 'B'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not 0 <= row1 < 8 or not 0 <= col1 < 8:
            return False

        if row == row1 or col == col1:
            return False

        # диагональная проверка
        row_step = 1 if (row1 > row) else -1
        col_step = 1 if (col1 > col) else -1
        r, c = row + row_step, col + col_step

        while row1 != r and col1 != c:
            if not (board.get_piece(r, c) is None):
                return False
            r += row_step
            c += col_step

        # путь свободен
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color
        self.was_moved = False

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        return abs(row - row1) <= 1 and abs(col - col1) <= 1

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    def __init__(self, color):
        self.color = color

    def can_move(self, board, row, col, row1, col1):
        if not 0 <= row1 < 8 or not 0 <= col1 < 8:
            return False
        if row == row1 and col == col1:
            return False
        if (abs(row - row1) != abs(col - col1)) and (
                row != row1 and col != col1):
            return False

        if col == col1:  # вертикальная проверка
            step = 1 if row1 >= row else -1
            for r in range(row + step, row1, step):
                if board.get_piece(r, col) is not None:
                    return False

        if row == row1:  # горизонтальная проверка
            step = 1 if col1 >= col else -1
            for c in range(col + step, col1, step):
                if board.get_piece(row, c) is not None:
                    return False

        elif row != row1 and col != col1:  # диагональная проверка
            row_step = 1 if row1 > row else -1
            col_step = 1 if col1 > col else -1
            r, c = row + row_step, col + col_step

            while r != row1 and c != col1:
                if board.field[r][c] is not None:
                    return False  # На пути есть фигура
                r += row_step
                c += col_step

        # можно съесть фигуру другого цвета
        piece = board.get_piece(row1, col1)
        if piece is not None:
            if self.color != piece.color:
                return True
            return False

        # путь свободен
        return True

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight:
    def __init__(self, color):
        self.color = color

    def char(self):
        return 'N'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if not 0 <= row1 < 8 or not 0 <= col1 < 8:
            return False
        if row == row1 or col == col1:
            return False
        if abs(row - row1) + abs(col - col1) != 3:
            return False
        # путь свободен
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

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
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)

        # для рокировки
        if piece.__class__.__name__ == 'Rook' or piece.__class__.__name__ == 'King':
            piece.was_moved = True
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        # проверяем, что фигура является пешкой
        if self.field[row][col].__class__.__name__ != 'Pawn':
            return False
        # проверяем, что можно сходить до конца доски
        if not self.move_piece(row, col, row1, col1):
            return False

        # ходим пешкой
        self.move_piece(row, col, row1, col1)
        color = self.field[row1][col1].color
        if char == 'Q':
            # меняем пешку на ферзя соответствующего цвета
            self.field[row1][col1] = Queen(color)
        elif char == 'R':
            # меняем пешку на ладью соответствующего цвета
            self.field[row1][col1] = Rook(color)
        elif char == 'B':
            # меняем пешку на слона соответствующего цвета
            self.field[row1][col1] = Bishop(color)
        elif char == 'N':
            # меняем пешку на коня соответствующего цвета
            self.field[row1][col1] = Knight(color)
        return True

    def castling0(self):
        row = 0 if self.color == WHITE else 7
        rook = self.field[row][0]
        king = self.field[row][4]

        # проверяем, что это нужные фигуры и фигуры не ходили
        if (
                rook.__class__.__name__ != 'Rook' or king.__class__.__name__ != 'King' or
                king.was_moved or rook.was_moved
        ):
            return False

        # проверяем, что пути свободны
        if any(self.field[row][i] is not None for i in range(1, 4)):
            return False

        # перемещаем короля и ладью
        self.field[row][3] = rook
        self.field[row][2] = king
        self.field[row][4] = None
        self.field[row][0] = None

        # фигурами походили
        rook.was_moved = True
        king.was_moved = True

        # меняем цвет игрока
        self.color = WHITE if self.color == BLACK else BLACK
        return True

    def castling7(self):
        row = 0 if self.color == WHITE else 7
        rook = self.field[row][7]
        king = self.field[row][4]

        # проверяем, что это нужные фигуры и фигуры не ходили
        if (
                rook.__class__.__name__ != 'Rook' or king.__class__.__name__ != 'King' or
                king.was_moved or rook.was_moved
        ):
            return False

        # проверяем, что пути свободны
        if any(self.field[row][i] is not None for i in range(5, 7)):
            return False

        # перемещаем короля и ладью
        self.field[row][5] = rook
        self.field[row][6] = king
        self.field[row][7] = None
        self.field[row][4] = None

        # фигурами походили
        rook.was_moved = True
        king.was_moved = True

        # меняем цвет игрока
        self.color = WHITE if self.color == BLACK else BLACK
        return True

    def get_piece(self, row, col):
        return self.field[row][col]


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


def print_board(board):
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


WHITE = 1
BLACK = 2
