#!/usr/bin/env python3


import copy


class TetrisPiece:
    '''A tetris piece generated in the game. It can be moved, rotated
    and placed in the play grid.
    
    Attributes
    ----------
        color : string
            A color of the shape
        state : list
            A list of shape\'s coordinates
        rotation_cycle : dictionary
            Mappings of where tiles should be when the piece is rotated
    '''

    def __init__(self, color, state, rotation_cycle):
        self.color = color
        self.current_state = state
        self.rotation_cycle = rotation_cycle
    
    def get_color(self):
        '''Returns shape\'s color'''

        return self.color
    
    def rotate(self):
        '''Returns next rotation shape.
        
        Returns
        -------
            new_state : list
                List of new coordinates
        '''
        
        new_state = []
        for tile in self.current_state:
            new_tile = copy.deepcopy(self.rotation_cycle[str(tile)])
            new_state.append(new_tile)
        
        self.current_state = new_state
    
    def get_current_state(self):
        '''Returns current shape\'s state as a list of tiles'''

        return self.current_state
    
    def move_down(self):
        '''Updates piece\'s current state to move it down'''

        self.modify_shape(row=1)
        self.modify_rotation_cycle(row=1)
    
    def move_left(self):
        '''Updates piece\'s current state to move it left'''

        self.modify_shape(column=-1)
        self.modify_rotation_cycle(column=-1)
    
    def move_right(self):
        '''Updates piece\'s current state to move it right'''

        self.modify_shape(column=1)
        self.modify_rotation_cycle(column=1)
    
    def modify_shape(self, row=0, column=0):
        '''Modifies piece\'s shape by rows or columns.
        
        Parameters
        ----------
            row : integer
                Number of row
            column : integer
                Number of column
        '''

        for tile in self.current_state:
            tile[0] += row
            tile[1] += column
    
    def modify_rotation_cycle(self, row=0, column=0):
        '''Modifies piece\'s rotation cycle by rows or columns.
        
        Parameters
        ----------
            row : integer
                Number of row
            column : integer
                Number of column
        '''

        modified_rotation = {}
        for tile1, tile2 in self.rotation_cycle.items():    
            tile1 = tile1.strip('][').split(', ')
            tile1[0] = int(tile1[0])
            tile1[1] = int(tile1[1])

            tile1[0] += row
            tile1[1] += column
            tile2[0] += row
            tile2[1] += column
            
            modified_rotation[str(tile1)] = tile2
        
        self.rotation_cycle = modified_rotation