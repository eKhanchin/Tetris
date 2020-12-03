#!/usr/bin/env python3

from collections import defaultdict
import copy
import random
from tkinter import Canvas
from tkinter import Text
from tkinter import Tk
from tkinter import ttk

from tetris_model import clear_piece
from tetris_model import create_game_pieces
from tetris_model import draw_piece
from tetris_model import initiate_piece_location
from tetris_piece import TetrisPiece


class Tetris:
    '''A classic tetris game.
    
    Attributes
    ----------
        master : object
            tkinter root window object
    '''

    def __init__(self, master):
        self.master = master
        master.title('Tetris')
        master.geometry('420x554+100+200')
        master.resizable(False, False)

        self._configure_style()

        canvas = Canvas(master, width=261, height=521,\
            relief='sunken', highlightthickness=1,\
            highlightbackground=self._grid_border_color)
        canvas.place(x=7, y=17)
        self._background_canvas = canvas

        self._create_welcome_screen()
        self._create_next_window()
        self._create_score_window()
    
    def _configure_style(self):
        '''Configures style of the application'''

        # Defines application's colors
        self._grid_start_color = '#272822'
        self._grid_play_color = '#6f7066'
        self._grid_border_color = '#46473d'
        self._play_button_color = '#229922'
        self._play_button_active_color = '#44c244'
        self._text_color = '#f2f2f2'
        self._next_frame_color = '#272822'
        self._tile_color = '#272822'
        self._colors = {'red': '#ff4d4d', 'orange': '#ffc966',
            'yellow': '#ffff4d', 'green': '#4dff4d',
            'purple': '#be90d4', 'blue': '#4a80ff', 'cyan': '#0cf0f0'}

        # Defines application's styles
        style = ttk.Style()
        style.configure('Tile.TLabel', background=self._tile_color,\
            relief='flat')

        # Play button style
        style.configure('Play.TButton', background=self._play_button_color,\
            foreground=self._text_color, font=('Calibri', 16, 'bold'))
        style.map('Play.TButton', background=[('active',\
            self._play_button_active_color)])

        # Game rules style
        style.configure('Rules.TLabel', background=self._grid_start_color,\
            foreground=self._text_color, font=('Calibri', 14))

        # Next and score windows style
        style.configure('NextScore.TFrame', relief='groove',\
            background=self._next_frame_color)
        style.configure('NextScore.TLabel', background=self._next_frame_color,\
            foreground=self._text_color, font=('Calibri', 14, 'bold'))
        style.configure('NextGrid.TLabel', background=self._tile_color,\
            relief='flat')

        # Time counter style
        style.configure('Timer.TLabel', background=self._grid_start_color,\
            foreground=self._text_color, font=('Calibri', 42, 'bold'))
        
        # Game over style
        style.configure('GameOver.TLabel', background=self._grid_start_color,\
            foreground=self._text_color, font=('Calibri', 32, 'bold'))
        style.configure('FinalScore.TLabel', background=self._grid_start_color,\
            foreground=self._text_color, font=('Calibri', 20, 'bold'))

    def _create_welcome_screen(self):
        '''Creates all fields relevant to welcome screen'''

        canvas = self._background_canvas
        canvas.configure(background=self._grid_start_color)

        # Title
        text = Text(canvas, height=1, relief='flat',\
            background=self._grid_start_color, foreground='white',\
            highlightthickness=0, font=('Calibri', 36, 'bold'))
        text.place(x=63, y=50, width=140)
        self._title_text = text
        self._color_title()
        
        # Play button
        button = ttk.Button(canvas, text='PLAY',\
            style='Play.TButton', command=self._prepare_for_game)
        button.place(x=57, y=186, width=150, height=30)
        self._play_button = button

        # Game rules
        left_arrow = canvas.create_line(12, 320, 32, 320,\
            width=5, arrow='first', fill=self._text_color)
        right_arrow = canvas.create_line(42, 320, 62, 320,\
            width=5, arrow='last', fill=self._text_color)
        up_arrow = canvas.create_line(37, 350, 37, 370,\
            width=5, arrow='first', fill=self._text_color)
        down_arrow = canvas.create_line(37, 390, 37, 410,\
            width=5, arrow='last', fill=self._text_color)
        
        self._arrows_images = [left_arrow, right_arrow, up_arrow, down_arrow]

        label = ttk.Label(canvas,\
            text='move the piece left or right', style='Rules.TLabel')
        label.place(x=81, y=310)
        self._move_rule_label = label

        label = ttk.Label(canvas,\
            text='rotate the piece', style='Rules.TLabel')
        label.place(x=81, y=350)
        self._rotate_rule_label = label

        label = ttk.Label(canvas,\
            text='place the piece', style='Rules.TLabel')
        label.place(x=81, y=390)
        self._place_rule_label = label

    def _color_title(self):
        '''Colours each character of a title in different color'''
        
        self._title_text.insert('1.0', 'TETRIS')
        self._title_text.tag_configure('red',\
            foreground=self._colors['red'])
        self._title_text.tag_add('red', '1.0', '1.1')
        self._title_text.tag_configure('orange',\
            foreground=self._colors['orange'])
        self._title_text.tag_add('orange', '1.1', '1.2')
        self._title_text.tag_configure('yellow',\
            foreground=self._colors['yellow'])
        self._title_text.tag_add('yellow', '1.2', '1.3')
        self._title_text.tag_configure('green',\
            foreground=self._colors['green'])
        self._title_text.tag_add('green', '1.3', '1.4')
        self._title_text.tag_configure('blue',\
            foreground=self._colors['blue'])
        self._title_text.tag_add('blue', '1.4', '1.5')
        self._title_text.tag_configure('purple',\
            foreground=self._colors['purple'])
        self._title_text.tag_add('purple', '1.5', '1.6')
    
    def _create_next_window(self):
        '''Creates a window where the next piece is displayed'''

        frame = ttk.Frame(self.master, style='NextScore.TFrame')
        frame.place(x=290, y=17, width=123, height=111)
        
        ttk.Label(frame, text='NEXT', style='NextScore.TLabel')\
            .place(x=40, y=10)

        self._create_next_grid(frame)
    
    def _create_next_grid(self, frame):
        '''Creates a grid where the next piece will be displayed.
        
        Parameters
        ----------
            frame : object
                tkinter ttk.frame object
        '''

        # 4x2 tiles for a picture of next piece
        start_x = 10
        label_x = start_x
        label_y = 50
        label_width = 20
        label_height = 20
        self._next_grid = []
        row = []
        for i in range(1, 11):
            label = ttk.Label(frame, text='', style='NextGrid.TLabel')
            label.place(x=label_x, y=label_y, width=label_width,\
                height=label_height)
            
            row.append(label)
            label_x += label_width + 1

            if i%5 == 0:
                self._next_grid.append(row)
                row = []
                label_y += label_height + 1
                label_x = start_x
    
    def _create_score_window(self):
        '''Creates a window where the score is displayed'''

        frame = ttk.Frame(self.master, style='NextScore.TFrame')
        frame.place(x=290, y=150, width=123, height=77)

        ttk.Label(frame, text='SCORE', style='NextScore.TLabel')\
            .place(x=35, y=10)
        label = ttk.Label(frame, text='', style='NextScore.TLabel',\
            anchor='center', width=10)
        label.place(x=21, y=50)
        self._score_label = label
    
    def _prepare_for_game(self):
        '''Prepares to start the game'''

        canvas = self._background_canvas

        self._delete_welcome_widgets()
        self._score_label.configure(text='0')
        self._pieces = create_game_pieces(self._colors)
        self._show_next_piece()

        timer_label = ttk.Label(canvas, text='4', style='Timer.TLabel')
        timer_label.place(x=120, y=150)
        self._timer_label = timer_label
        self._set_timer()
    
    def _delete_welcome_widgets(self):
        '''Deletes welcome screen's widgets'''

        canvas = self._background_canvas

        self._title_text.destroy()
        self._play_button.destroy()
        self._move_rule_label.destroy()
        self._rotate_rule_label.destroy()
        self._place_rule_label.destroy()

        for arrow in self._arrows_images:
            canvas.delete(arrow)
    
    def _create_play_grid(self):
        '''Creates playground grid'''

        canvas = self._background_canvas

        # Dimensions of the grid
        self._left = 0
        self._up = 0
        self._right = 9
        self._down = 19

        self._grid_width = 10
        grid_height = 20

        # 20x10 tiles of a playground grid
        start_x = 2
        label_x = start_x
        label_y = 2
        label_width = 25
        label_height = 25
        self._play_grid = []
        row = []
        tiles_amount = self._grid_width*grid_height + 1
        for i in range(1, tiles_amount):
            label = ttk.Label(canvas, text='', style='Tile.TLabel')
            label.place(x=label_x, y=label_y, width=label_width,\
                height=label_height)

            row.append(label)
            label_x += label_width + 1

            if i%(self._right+1) == 0:
                self._play_grid.append(row)
                row = []
                label_y += label_height + 1
                label_x = start_x
    
    def _show_next_piece(self):
        '''Displays next tetris piece'''
        
        # Clears next grid
        for row in self._next_grid:
            for tile in row:
                tile.configure(background=self._tile_color)

        self._next_piece = copy.deepcopy(random.choice(self._pieces))
        draw_piece(self._next_piece, self._next_grid)
    
    def _set_timer(self):
        '''Sets a time counter for 3 seconds'''

        time = int(self._timer_label.cget('text'))
        time -= 1
        if time == 0:
            self.master.after_cancel(self._job)
            self._job = None

            self._timer_label.destroy()
            self._start_game()
            return

        self._timer_label.config(text=f'{time}')
        self._job = self.master.after(1000, self._set_timer)
    
    def _start_game(self):
        '''Starts the game'''

        canvas = self._background_canvas

        # Initializes the game's attributes
        self._create_play_grid()
        canvas.configure(background=self._grid_play_color)
        
        self._set_current_piece()
        self._show_next_piece()
        self._score = 0

        # Represents tiles that are colored, where the pieces are placed
        self._taken_tiles = defaultdict(bool)

        # Movement, rotation and placement bind keys
        self.master.bind('<Left>', lambda e: self._update_piece_state('left'))
        self.master.bind('<Right>', lambda e: self._update_piece_state('right'))
        self.master.bind('<Up>', lambda e: self._update_piece_state('rotate'))
        self.master.bind('<Down>', lambda e: self._update_piece_state('down'))

        # Starts to move current piece down
        self._move_piece_down()
    
    def _move_piece_down(self):
        '''Moves a piece down'''

        got_to_taken_tiles = self._got_to_taken_tiles()

        if got_to_taken_tiles == 1:
            # Piece is placed, goes to the next piece
            self._update_taken_tiles()
            self._check_filled_rows()
            self._set_current_piece()
            self._show_next_piece()
        elif got_to_taken_tiles == -1:
            # Game over
            self.master.after_cancel(self._job)
            self._job = None

            self._clear_play_screen()
            self._create_game_over_screen()

            return
        
        # Continues to move piece down
        self._update_piece_state('down')
        
        self._job = self.master.after(300, self._move_piece_down)
    
    def _update_piece_state(self, operation):
        '''Updates piece\'s current state according to provoked
        operation.
        
        Parameters
        ----------
            operation : string
                An operation - down/left/right/rotate
        '''
        
        piece = self._current_piece

        clear_piece(piece, self._play_grid, self._tile_color)

        if operation == 'down':
            if self._is_moved_in_boundaries(piece, operation)\
                    and self._got_to_taken_tiles() == 0:
                piece.move_down()
        elif operation == 'left':
            if self._is_moved_in_boundaries(piece, operation):
                piece.move_left()
        elif operation == 'right':
            if self._is_moved_in_boundaries(piece, operation):
                piece.move_right()
        elif operation == 'rotate':
            piece.rotate()
            self._correct_rotated_shape()

        draw_piece(piece, self._play_grid)

    def _got_to_taken_tiles(self):
        '''Checks whether current piece has gotten to the surface.
        
        Returns
        -------
            flag : boolean
                -1 - got to surface and it\'s a game over
                0 - not on the surface yet
                1 - got to surface 
        '''

        shape = self._current_piece.get_current_state()
        for tile in shape:
            row = tile[0]

            is_taken = self._is_tile_taken(tile, next_row=1)

            if row+1 > self._down or is_taken:
                # Got to lowest part of the grid or the next tile is
                # taken
                if row==0 or row==1:
                    return -1

                return 1
        
        return 0
    
    def _update_taken_tiles(self):
        '''Updates surface with current piece\'s tiles'''
        
        shape = self._current_piece.get_current_state()
        for tile in shape:
            row = tile[0]
            column = tile[1]

            tile_number = row*self._grid_width + column
            
            # The tile with tile_number is taken from now on
            self._taken_tiles[tile_number] = True
                    
    def _is_moved_in_boundaries(self, piece, direction):
        '''Checks whether current piece is in grid boundries.
        
        Parameters
        ----------
            piece : object
                TetrisPiece object
            direction : string
                Direction of movement
        
        Return
        ------
            flag : bool
                Is piece in the boundaries
        '''

        shape = self._current_piece.get_current_state()
        for tile in shape:
            row = tile[0]
            column = tile[1]

            is_left_taken = self._is_tile_taken(tile, next_column=-1)
            is_right_taken = self._is_tile_taken(tile, next_column=2)

            if direction == 'down' and row+1 > self._down:
                return False
            if direction == 'left' and (column-1 < self._left\
                    or is_left_taken):
                return False
            if direction == 'right' and (self._right < column+1\
                    or is_right_taken):
                return False
        
        return True
    
    def _set_current_piece(self):
        '''Sets next piece to be current'''

        self._current_piece = self._next_piece
        initiate_piece_location(self._current_piece)
    
    def _check_filled_rows(self):
        '''Checks whether there are filled rows, rows that are fully
        colored'''

        # Rows that need to be checked
        rows = [tile[0] for tile in
            self._current_piece.get_current_state()]
        
        while rows:
            row = rows[0]
            left_tile_number = row * self._grid_width
            right_tile_number = left_tile_number + self._grid_width - 1

            # All filled tiles in a checked row
            filled_tile_numbers = [tile_number for tile_number
                in self._taken_tiles
                if self._taken_tiles[tile_number]
                and left_tile_number<=tile_number
                and tile_number<=right_tile_number]
            
            # If row is fully filled
            if len(filled_tile_numbers) == self._grid_width:
                self._update_score()
                self._delete_filled_row(row)
                self._delete_from_taken_tiles(filled_tile_numbers)
                self._move_filled_tiles_down(row)
            else:
                del rows[0]
    
    def _update_score(self):
        '''Updates the score when row is filled'''

        self._score += 100
        self._score_label.configure(text=str(self._score))

    def _delete_filled_row(self, row):
        '''Deletes filled row from a grind.
        
        Parameters
        ----------
            row : integer
                Number of a row
        '''

        for column in range(self._grid_width):
            self._play_grid[row][column]\
                .configure(background=self._tile_color)
    
    def _delete_from_taken_tiles(self, filled_tile_numbers):
        '''Deletes given filled tiles from a taken tiles dictionary.
        
        Parameters
        ----------
            filled_tile_numbers : list
                List of tile numbers
        '''

        for tile_number in filled_tile_numbers:
            self._taken_tiles[tile_number] = False
    
    def _move_filled_tiles_down(self, row_number):
        '''Moves filled tiles above the filled row down in the play
        grid.
        
        Parameters
        ----------
            row_number : integer
                Number of a row
        '''

        for row in range(row_number, -1, -1):
            for column in range(self._grid_width):
                color = str(self._play_grid[row][column].cget('background'))

                if color and color!=self._tile_color:
                    # Moves colored tile down
                    self._play_grid[row][column]\
                        .configure(background=self._tile_color)
                    self._play_grid[row+1][column].configure(background=color)

                    # Deletes previous tile from taken tiles
                    tile_number = row*self._grid_width + column
                    self._taken_tiles[tile_number] = False

                    # Adds next tile to taken tiles
                    tile_number += self._grid_width
                    self._taken_tiles[tile_number] = True
    
    def _correct_rotated_shape(self):
        '''Corrects current shape\'s coordinates, so they will not pass
        the boundaries of the play grid'''

        steps_to_move = 0
        shape = self._current_piece.get_current_state()

        for tile in shape:
            column = tile[1]

            if column < self._left:
                # Shape passed left border
                delta = self._left - column
                if delta > steps_to_move:
                    steps_to_move = delta
            elif self._right < column:
                # Shape passed right border
                delta = self._right - column
                if delta < steps_to_move:
                    steps_to_move = delta
        
        # Moves shape left or right, so it will be inside borders
        if steps_to_move != 0:
            self._current_piece.modify_shape(column=steps_to_move)
            self._current_piece.modify_rotation_cycle(column=steps_to_move)
    
    def _is_tile_taken(self, tile, next_row=0, next_column=0):
        '''Checks whether a given tile is taken already.
        
        Parameters
        -----------
            tile : list
                A tile in a grid
            (optional) next_row : integer
                Which row to check
            (optional) next_column : integer
                Which column to check
        
        Returns
        -------
            is_taken : boolean
                A tile is (not) taken
        '''

        row = tile[0] + next_row
        column = tile[1] + next_column
        next_tile_number = row*self._grid_width + column

        return self._taken_tiles[next_tile_number]
    
    def _clear_play_screen(self):
        '''Clears play screen from all widgets'''

        # Disables movement, rotation and placement bind keys
        self.master.unbind('<Left>')
        self.master.unbind('<Right>')
        self.master.unbind('<Up>')
        self.master.unbind('<Down>')

        # Deletes play grid tiles
        for row in self._play_grid:
            for tile in row:
                tile.destroy()
        
        # Changes background color of canvas back to start color
        self._background_canvas.configure(background=self._grid_start_color)

        # Clear next grid
        for row in self._next_grid:
            for tile in row:
                tile.configure(background=self._tile_color)
        
        # Nullifies the score
        self._score_label.configure(text='0')

    def _create_game_over_screen(self):
        '''Creates game over screen'''

        canvas = self._background_canvas

        label = ttk.Label(canvas, text='GAME OVER', style='GameOver.TLabel')
        label.place(x=30, y=50)
        self._game_over_label = label

        label = ttk.Label(canvas, text='Your final score is:',\
            style='FinalScore.TLabel')
        label.place(x=36, y=130)
        self._final_score_text_label = label

        label = ttk.Label(canvas, text=f'{self._score}',\
            style='FinalScore.TLabel', anchor='center', width=10)
        label.place(x=71, y=170)
        self._final_score_label = label
        
        # Play button
        button = ttk.Button(canvas, text='PLAY AGAIN', style='Play.TButton',\
            command=self._restart_game)
        button.place(x=57, y=250, width=150, height=30)
        self._play_again_button = button
    
    def _restart_game(self):
        '''Restarts the game'''

        self._clear_game_over_screen()
        self._prepare_for_game()
    
    def _clear_game_over_screen(self):
        '''Deletes all game over widgets'''
        
        self._game_over_label.destroy()
        self._final_score_text_label.destroy()
        self._final_score_label.destroy()
        self._play_again_button.destroy()


def main():
    root = Tk()
    app = Tetris(root)
    root.mainloop()


if __name__ == '__main__':
    main()