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

        else:  # диагональная проверка
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