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

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)