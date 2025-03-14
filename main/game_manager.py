from copy import deepcopy
import numpy
import random

# Custom modules
from main.colors import get_color_number
from main.grid import Grid
from main.pieces import create_game_pieces


class GameManager:
    """ A game manager responsible for piece movement and rotation on a
    grid, clearing grid and counting score.
    """
    def __init__(self):
        self.grid = Grid()
        self.board = self.grid.board
        self.board_height = self.grid.height
        self.board_width = self.grid.width
        self.piece = None
        
        self.pieces = create_game_pieces()
        self.next_piece = deepcopy(random.choice(self.pieces))
        self._set_new_piece()
    
    def _set_piece_initial_location(self):
        middle = self.board_width // 2 - 1
        for cell in self.piece.shape:
            cell[0] -= 1
            cell[1] += middle
    
    def _update_board(self):
        for row, column in self.piece.shape:
            if row >= 0:
                self.board[row][column] = get_color_number(self.piece.color)
    
    def _clear_previous_location(self):
        for row, column in self.piece.shape:
            if row >= 0:
                self.board[row][column] = 0
    
    def _get_bottom_cells(self) -> list:
        min_column = min(cell[1] for cell in self.piece.shape)
        max_column = max(cell[1] for cell in self.piece.shape)
        bottom_cells = []
        
        # Group by columns
        for column in range(min_column, max_column+1):
            rows = [cell for cell in self.piece.shape if cell[1] == column]
            bottom_row = max(cell[0] for cell in rows)
            bottom_cells.append([bottom_row, column])
            
        return bottom_cells
    
    def _get_right_cells(self) -> list:
        min_row = min(cell[0] for cell in self.piece.shape)
        max_row = max(cell[0] for cell in self.piece.shape)
        right_cells = []
        
        # Group by rows
        for row in range(min_row, max_row+1):
            columns = [cell for cell in self.piece.shape if cell[0] == row]
            right_column = max(cell[1] for cell in columns)
            right_cells.append([row, right_column])
        
        return right_cells
    
    def _get_left_cells(self) -> list:
        min_row = min(cell[0] for cell in self.piece.shape)
        max_row = max(cell[0] for cell in self.piece.shape)
        left_cells = []
        
        # Group by rows
        for row in range(min_row, max_row+1):
            columns = [cell for cell in self.piece.shape if cell[0] == row]
            left_column = min(cell[1] for cell in columns)
            left_cells.append([row, left_column])
        
        return left_cells
    
    def _update_piece_location(self, row_value: int, column_value: int):
        self._clear_previous_location()
        
        for cell in self.piece.shape:
            cell[0] += row_value
            cell[1] += column_value
            
        self._update_board()
    
    def _set_new_piece(self):
        """ Selects a new piece randomly from the available pieces and
        sets it as the current piece.
        """
        
        self.piece = deepcopy(self.next_piece)
        self._set_piece_initial_location()
        
        self.next_piece = deepcopy(random.choice(self.pieces))
    
    def _is_occupied(self, row: int, col: int) -> bool:
        return self.board[row][col] != 0 and [row, col] not in self.piece.shape
    
    def _rotatable(self, row: int, col: int) -> bool:
        if col < 0 or col >= self.board_width:
            return False
        
        if row >= 0 and row < self.board_height and self._is_occupied(row, col):
            return False
        
        return True
    
    def clear_filled_lines(self) -> int:
        """ Clears fully filled lines from the game board and shifts the
        rows above down to fill the cleared space.

        Returns:
            int: The number of rows that were cleared from the board.
        """

        cleared_rows = 0
        new_board = numpy.zeros_like(self.board, dtype=numpy.int32)
        new_row_index = self.board_height - 1

        for row_index in range(self.board_height-1, -1, -1):
            row = self.board[row_index]
            if not all(value != 0 for value in row):
                new_board[new_row_index] = row
                new_row_index -= 1
            else:
                cleared_rows += 1

        self.board = new_board
        return cleared_rows
    
    def is_game_over(self) -> bool:
        """ Checks if the game is over by determining if any part of
        the board's top row is occupied.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        
        top_row = self.board[0]
        return any(value != 0 for value in top_row)
    
    def move_right(self):
        """ Moves game piece right within game's grid. """
        
        for cell in self._get_right_cells():
            row, column = cell
            if column+1 >= self.board_width or (row >= 0 and self.board[row][column+1] != 0):
                return
            
        self._update_piece_location(0, 1)
    
    def move_left(self):
        """ Moves game piece left within game's grid. """
        
        for cell in self._get_left_cells():
            row, column = cell
            if column-1 < 0 or (row >= 0 and self.board[row][column-1] != 0):
                return
            
        self._update_piece_location(0, -1)
    
    def move_down(self) -> bool:
        """ Moves game piece down by 1 cell.
        
        Indicates whether the piece reached the bottom of the board or
        a colored cell.
        
        Returns:
            bool: Whether a piece is down.
        """

        for cell in self._get_bottom_cells():
            row, column = cell
            if row+1 >= self.board_height or self.board[row+1][column] != 0:
                self._set_new_piece()
                return True
        
        self._update_piece_location(1, 0)
        
        return False
    
    def rotate(self):
        """ Rotates game piece in 90 degrees within game's grid. """
        pivot_cell = self.piece.get_pivot_cell()
        if not pivot_cell:
            return
        
        pivot_row, pivot_col = pivot_cell
        new_shape = []
        
        for row, col in self.piece.shape:
            new_row = (col - pivot_col) + pivot_row
            new_col = -(row - pivot_row) + pivot_col
            if not self._rotatable(new_row, new_col):
                return
            
            new_shape.append([new_row, new_col])
        
        self._clear_previous_location()
        self.piece.shape = new_shape
        self._update_board()
