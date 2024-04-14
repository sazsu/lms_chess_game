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
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)
