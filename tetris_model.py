#!/usr/bin/env python3

from tetris_piece import TetrisPiece


def create_game_pieces(colors):
        '''Creates game\'s pieces.
        
        Parameters
        ----------
            colors : dictionary
                A dictionary of colors - name: color
        
        Returns
        -------
            pieces : list
                A list of game\'s pieces
        '''

        pieces = []

        #   ##
        # ######     
        color = colors['purple']
        state = [[0, 2], [1, 1], [1, 2], [1, 3]]
        rotation_cycle = {'[0, 2]': [1, 3], '[1, 1]': [0, 2], '[1, 2]': [1, 2],
                        '[1, 3]': [2, 2], '[2, 2]': [1, 1]}

        piece = TetrisPiece(color, state, rotation_cycle)
        pieces.append(piece)

        #     ##
        # ######
        color = colors['orange']
        state = [[0, 3], [1, 1], [1, 2], [1, 3]]
        rotation_cycle = {'[0, 3]': [2, 3], '[1, 1]': [0, 2], '[1, 2]': [1, 2],
                        '[1, 3]': [2, 2], '[2, 3]': [2, 1], '[0, 2]': [1, 3],
                        '[2, 2]': [1, 1], '[2, 1]': [0, 1], '[0, 1]': [0, 3]}

        piece = TetrisPiece(color, state, rotation_cycle)
        pieces.append(piece)

        #   ####
        # ####
        color = colors['green']
        state = [[0, 2], [0, 3], [1, 1], [1, 2]]
        rotation_cycle = {'[0, 2]': [1, 3], '[0, 3]': [2, 3], '[1, 1]': [0, 2],
                        '[1, 2]': [1, 2], '[1, 3]': [2, 2], '[2, 3]': [2, 1],
                        '[2, 2]': [1, 1], '[2, 1]': [0, 1], '[0, 1]': [0, 3]}

        piece = TetrisPiece(color, state, rotation_cycle)
        pieces.append(piece)

        # ##
        # ######
        color = colors['blue']
        state = [[0, 1], [1, 1], [1, 2], [1, 3]]
        rotation_cycle = {'[0, 1]': [0, 3], '[1, 1]': [0, 2], '[1, 2]': [1, 2],
                        '[1, 3]': [2, 2], '[0, 3]': [2, 3], '[0, 2]': [1, 3],
                        '[2, 2]': [1, 1], '[2, 3]': [2, 1], '[2, 1]': [0, 1]}

        piece = TetrisPiece(color, state, rotation_cycle)
        pieces.append(piece)

        # ####
        #   ####
        color = colors['red']
        state = [[0, 1], [0, 2], [1, 2], [1, 3]]
        rotation_cycle = {'[0, 1]': [0, 3], '[0, 2]': [1, 3], '[1, 2]': [1, 2],
                        '[1, 3]': [2, 2], '[0, 3]': [2, 3], '[2, 2]': [1, 1],
                        '[2, 3]': [2, 1], '[1, 1]': [0, 2], '[2, 1]': [0, 1]}

        piece = TetrisPiece(color, state, rotation_cycle)
        pieces.append(piece)

        # ####
        # ####
        color = colors['yellow']
        state = [[0, 1], [0, 2], [1, 1], [1, 2]]
        rotation_cycle = {'[0, 1]': [0, 1], '[0, 2]': [0, 2], '[1, 1]': [1, 1],
                        '[1, 2]': [1, 2]}

        piece = TetrisPiece(color, state, rotation_cycle)
        pieces.append(piece)

        # ########
        color = colors['cyan']
        state = [[1, 0], [1, 1], [1, 2], [1, 3]]
        rotation_cycle = {'[1, 0]': [0, 2], '[1, 1]': [1, 2], '[1, 2]': [2, 2],
                        '[1, 3]': [3, 2], '[0, 2]': [2, 3], '[2, 2]': [2, 1],
                        '[3, 2]': [2, 0], '[2, 3]': [3, 1], '[2, 1]': [1, 1],
                        '[2, 0]': [0, 1], '[3, 1]': [1, 3], '[0, 1]': [1, 0]}

        piece = TetrisPiece(color, state, rotation_cycle)
        pieces.append(piece)

        return pieces


def draw_piece(piece, grid):
        '''Draws a piece in a grid according to piece\'s current state.
        
        Parameters
        ----------
            piece : object
                TetrisPiece object
            grid : list
                List of grid tiles
        '''

        color = piece.get_color()
        shape = piece.get_current_state()

        for tile in shape:
            row = tile[0]
            column = tile[1]

            if row >= 0:
                # Grid contains labels
                grid[row][column].configure(background=color)


def clear_piece(piece, grid, color):
        '''Clears a piece from a grid according to piece\'s current state.
        
        Parameters
        ----------
            piece : object
                TetrisPiece object
            grid : list
                List of grid tiles
            color : string
                Background color
        '''

        shape = piece.get_current_state()

        for tile in shape:
            row = tile[0]
            column = tile[1]

            if row >= 0:
                # Grid contains labels
                grid[row][column].configure(background=color)


def initiate_piece_location(piece):
    '''Initiates piece\'s location to be in the center of the play
    grid.
    
    Parameters
    ----------
        piece : object
            TetrisPiece object
    '''

    piece.modify_shape(row=-2, column=3)
    piece.modify_rotation_cycle(row=-2, column=3)