class Rook:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку,
        # которая не лежит в том же ряду или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if row1 > row else -1
        for r in range(row + step, row1, step):
            # Если на пути по вертикали есть фигура
            if board.get_piece(r, col) is not None:
                return False

        step = 1 if col1 >= col else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if board.get_piece(row, c) is not None:
                return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)