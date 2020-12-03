#!/usr/bin/env python3

from tkinter import Tk
from tkinter import ttk
import unittest

from tetris_model import clear_piece
from tetris_model import create_game_pieces
from tetris_model import draw_piece
from tetris_model import initiate_piece_location


def create_play_grid():
        '''Creates playground grid'''

        master = Tk()

        # 20x10 tiles of a playground grid
        start_x = 2
        label_x = start_x
        label_y = 2
        label_width = 25
        label_height = 25
        play_grid = []
        row = []
        for i in range(1, 201):
            label = ttk.Label(master, text='')

            row.append(label)
            label_x += label_width + 1

            if i%10 == 0:
                play_grid.append(row)
                row = []
                label_y += label_height + 1
                label_x = start_x
        
        return play_grid


class TestTetrisModel(unittest.TestCase):
    def test_pieces_amount(self):
        '''Tests whether all the 7 pieces are created'''

        colors = {'red': '#ff4d4d', 'orange': '#ffc966', 'yellow': '#ffff4d',
            'green': '#4dff4d', 'purple': '#be90d4', 'blue': '#4d4dff',
            'cyan': '#0cf0f0'}
        pieces = create_game_pieces(colors)

        self.assertEqual(len(pieces), 7)
    
    def test_piece_drawn(self):
        '''Tests whether the piece is drawn on the grid'''

        colors = {'red': '#ff4d4d', 'orange': '#ffc966', 'yellow': '#ffff4d',
            'green': '#4dff4d', 'purple': '#be90d4', 'blue': '#4d4dff',
            'cyan': '#0cf0f0'}
        pieces = create_game_pieces(colors)
        piece = pieces[0]
        grid = create_play_grid()

        draw_piece(piece, grid)
        color = piece.get_color()
        shape = piece.get_current_state()
        tile = shape[0]
        background_color = str(grid[tile[0]][tile[1]].cget('background'))

        self.assertEqual(background_color, color)
    
    def test_piece_cleared(self):
        '''Tests whether the piece is cleared from the grid'''

        colors = {'red': '#ff4d4d', 'orange': '#ffc966', 'yellow': '#ffff4d',
            'green': '#4dff4d', 'purple': '#be90d4', 'blue': '#4d4dff',
            'cyan': '#0cf0f0'}
        pieces = create_game_pieces(colors)
        piece = pieces[0]
        grid = create_play_grid()
        draw_piece(piece, grid)

        color = '#ffffff'
        clear_piece(piece, grid, color)

        shape = piece.get_current_state()
        tile = shape[0]
        background_color = str(grid[tile[0]][tile[1]].cget('background'))

        self.assertEqual(background_color, color)
    
    def test_initiate_piece_position_row(self):
        '''Tests whether piece\'s row position is initiated'''

        colors = {'red': '#ff4d4d', 'orange': '#ffc966', 'yellow': '#ffff4d',
            'green': '#4dff4d', 'purple': '#be90d4', 'blue': '#4d4dff',
            'cyan': '#0cf0f0'}
        pieces = create_game_pieces(colors)
        piece = pieces[0]

        row = piece.get_current_state()[0][0]
        initiate_piece_location(piece)
        new_row = piece.get_current_state()[0][0]

        row_delta = new_row - row

        self.assertEqual(row_delta, -2)
    
    def test_initiate_piece_position_column(self):
        '''Tests whether piece\'s column position is initiated'''

        colors = {'red': '#ff4d4d', 'orange': '#ffc966', 'yellow': '#ffff4d',
            'green': '#4dff4d', 'purple': '#be90d4', 'blue': '#4d4dff',
            'cyan': '#0cf0f0'}
        pieces = create_game_pieces(colors)
        piece = pieces[0]

        column = piece.get_current_state()[0][1]
        initiate_piece_location(piece)
        new_column = piece.get_current_state()[0][1]

        column_delta = new_column - column

        self.assertEqual(column_delta, 3)


if __name__ == '__main__':
    unittest.main()