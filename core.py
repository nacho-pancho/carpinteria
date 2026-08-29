#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Core carpentry library

Here we find definitions of things such as Size, Volume, Margin, Padding, the base Piece class,
the base CompositePiece class, and the different Layout methods.

Geometry-related definitions favor clarity over performance. This is not a computationally-intensive
library so we don't care about adding vectors by hand as long as each element has a clear meaning.

"""

import copy
from dataclasses import dataclass
import math

from jsonable import *
from util import *
from geometry import *
from  materials import *

        
#
# ==========================================================
# Core types
# ==========================================================
#

class Piece(JSONable):
    """
    base class for pieces
    """
    def __init__(self, 
                 name:str, 
                 material:Material,
                 fixed_size:Size=Size(None,None,None),
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 ):
        self.name = name
        self.material = material
        self.min_size = copy.deepcopy(min_size) 
        self.max_size = copy.deepcopy(max_size)
        self.volume = Volume(copy.deepcopy(fixed_size),Vector())
        # fixed_size overrides min_size and max_size 
        for i in range(3):
            if fixed_size[i] is not None:
                self.min_size.dim[i] = self.max_size.dim[i] = fixed_size[i]


    def __str__(self):
        return f'''Piece {self.name} made of {self.material}\
 at offset {self.volume.offset} size {self.volume.size}\
 (minimum size {self.min_size} \
 and maximum size {self.max_size}).'''
    
    def translate(self,t:Vector):
        self.offset.translate(t)

    def rotate(self,axis:float, angle:float):
        x,y,z = self.offset[:]
        if axis == X_COORD:
            new_x = x
            new_y = y*math.cos(angle) + -z*math.sin(angle)
            new_z = y*math.sin(angle) +  z*math.cos(angle)
        elif axis == Y_COORD:
            new_x = x*math.cos(angle) + -z*math.sin(angle)
            new_y = y
            new_z = x*math.sin(angle) +  z*math.cos(angle)
        elif axis == Z_COORD:
            new_x = x*math.cos(angle) + -y*math.sin(angle)
            new_y = x*math.sin(angle) +  y*math.cos(angle)
            new_z = z
        self.offset = [new_x,new_y,new_z]


    
    def part_description(self):
        """
        for building a list of parts
        """
        raise NotImplementedError()


    def part_list(self):
        """
        for building part lists
        besides the piece itself, or parts in a composite piece
        might include additional things like screws 
        """
        raise NotImplementedError()


    def __tojson__(self)->dict:
        d = super().__tojson__()
        d["name"] = self.name
        d["material"] =  self.material.__json__()
        d["min_size"] =  self.min_size.__json__()
        d["max_size"] =  self.max_size.__json__()
        d["volume"]   =    self.volume.__json() 
        return d

    def __fromjson__(d:dict): # class method
        raise NotImplementedError()
    
#--------------------------------------------------------------------

class Void(Piece):

    """ 
    a void piece is a piece that is not printed.
    """

    def __init__(self, 
                 fixed_size:Size=Size(None,None,None),
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 ):
        super().__init__(name='void', 
                         material=None, 
                         fixed_size=fixed_size,
                         min_size=min_size,
                         max_size=max_size)

    def part_list():
        return []


    def description(self)->str:
        """
        all voids are equal
        """
        return self.typename()
    
    def __fromjson__(d:dict):
        min_size = Size.__fromjson__(d['min_size'])
        max_size = Size.__fromjson__(d['max_size'])
        return Void(min_size=min_size,max_size=max_size)
                

#--------------------------------------------------------------------

class LayoutConstraints(JSONable):
    """
    Contains some information about how
    to put a piece inside of it, such as margins to the sides, padding, alignment in all directions.
    For some layout methods it also contains a 'weight' which is between 0 and 1. If space needs to 
    be shared between objects, then this specifies how much of the space should be taken, if possible.
    Weight is a soft constraint; hard constraints such as minimum and fixed sizes prevail, if defined.
    """

    def __init__(self):
        self.padding = Padding()
        self.margin = Margin()
        self.weight = [1,1,1]
        self.alignment = [CENTER,CENTER,CENTER]

    def __str__(self):
        return f'''LayoutConstraints:\
 {self.padding}\
 {self.margin} weight {self.weight}\
 alignment {self.alignment}'''

    def __tojson__(self):
        return {'padding': self.padding.__tojson__(self),
                'margin': self.margin.__tojson__(self),
                'weight': self.weight,
                'alignment': self.alignment}

    def __fromjson__(d:dict):
        padding = Padding.__fromjson__(d['padding'])
        margin  = Margin.__fromjson__(d['margin'])
        weight = d['weight']
        alignment = d['alignment']

#--------------------------------------------------------------------

class Part(JSONable):
    """
    part of a multi-piece object
    """

    def __init__(self,piece:Piece,constraints:LayoutConstraints):
        self.slot_volume = Volume()
        self.padded_volume = Volume()
        self.available_volume = Volume()
        self.piece_volume = Volume()
        self.piece = piece
        self.constraints = constraints

    def __str__(self):
        return f'Part:\n\t{self.piece}\n\t{self.constraints}'

    def __tojson__(self)->dict:
        d = super().__tojson__()
        d['piece'] = self.piece.__json__(),
        d['constraints'] = self.constraints.__json__()
        return d

    def __fromjson__(d:dict):
        return Part(Piece.__fromjson__(d['piece']),LayoutConstraints.__fromjson__(d['constraints']))

#--------------------------------------------------------------------

class Layout(JSONable):
    """
    Strategy or method by which pieces are put inside a composite piece.
    This is a typical concept in UI design. I'm copying it here.
    """
    def __init__(self):
        pass

    def apply(self, composite: CompositePiece):
        pass

    def slots(self):
        return 1


    def __tojson__(self):
        d = super.__tojson__()
        d['slots'] = self.slots()
        return d

    def __fromjson__():
        raise NotImplementedError
    
#--------------------------------------------------------------------

def simple_layout(_volume:Volume, part:Part):
    logger = get_logger()
    logger.info(f'Layoing out part {part.piece} within  {_volume} with coinstraints {part.constraints}')

    piece = part.piece
    cons  = part.constraints
    #
    # there are three volumes:
    # the slot volume; that is the total size inside the volume in this case
    # the padded volume, which results from the base volume being grown by the padding
    # the available volume, which results from the padded volume being reduced by the margins
    #
    # we keep track of them all
    part.base_volume = copy.deepcopy(_volume)
    logger.info(f'Base volume {part.base_volume}')
    part.slot_volume = copy.deepcopy(part.base_volume)
    # apply weights
    for i in range(3):
        part.slot_volume.size.dim[i] *= cons.weight[i]

    logger.info(f'Slot volume {part.slot_volume} after applying weight')
    part.padded_volume = grow_volume(part.slot_volume,cons.padding)
    logger.info(f'Padded volume {part.padded_volume}')
    part.available_volume = shrink_volume(part.padded_volume,cons.margin)
    logger.info(f'Available volume {part.available_volume}')
    #
    # we must reserve space for the margin, but this includes padding
    #
    margin_size = cons.margin.size()
    reserved_size = shrink_size(margin_size,cons.padding)
    # now we have the available volume
    # we take into account the piece's own constraints (min and max size)
    # to determine its final size
    # the margin is rigid so it needs to be taken into account in min_size

    piece_size = Size()
    for i in range(3):
        _min = piece.min_size.dim[i]
        _max = piece.max_size.dim[i]
        _ava = part.available_volume.size.dim[i]
        if _min  > _ava:
            logger.warning(f'Available space {_ava} not enough for min size {_min}!')
        piece_size.dim[i] = max(_min, min(_ava,_max))

    part.piece.volume = Volume(piece_size,copy.deepcopy(part.available_volume.offset))

    logger.info(f'Piece volume {part.piece.volume} (prior to alignment)')
    for i in range(3):
        delta = (part.available_volume.size.dim[i] - part.piece.volume.size.dim[i])
        logger.info(f'Excess volume at dimension {i} is {delta}')
        if cons.alignment[i] == CENTER:
            logger.info(f'Center alignment implies displacement by {delta/2}.')
            part.piece.volume.offset.coords[i] += delta / 2
        elif cons.alignment[i] == RIGHT or cons.alignment == BACK or cons.alignment == TOP:
            logger.info(f'right/top/back alignment implies displacement by {delta}.')
            part.piece.volume.offset.coords[i] += delta
    #
    # the final part is the placement of the piece if the piece
    # is smaller than the effective volume, it needs to be arranged
    # according to the alignment
    # 
    # put the piece according to the constraints
    part.piece_volume = part.piece.volume
    logger.info(f'Final volume {piece.volume} (after alignment)')


#--------------------------------------------------------------------

class DefaultLayout(Layout):
    """
    puts one thing inside
    """
    def __init__(self):
        pass

    def apply(self, _volume:Volume, _parts:tuple[Part]):

        logger = get_logger()
        logger.info(f'Applying layout {self} to volume {_volume}')
        # determine size of object
        if _parts[0] is None:
            logger.info(f'No parts to lay out.')
            return
        simple_layout(_volume,_parts[0])


    def slots(self):
        return 1

    def __str__(self):
        return 'Default layout'

    def __fromjson__(d:dict):
        return DefaultLayout()


#--------------------------------------------------------------------

class StackLayout(Layout): 
    """ 
    splits a volume into a vertical pile of slices along the Z axis
    """

    def __init__(self,num_slots:int,axis:int):
        self.num_slots = num_slots
        self.axis = axis
        if axis != X_COORD and axis != Y_COORD and axis != Z_COORD:
            raise ValueError(f'Invalid axis {axis}.')

    def slots(self):
        return self.num_slots

    def __str__(self):
        return f'StackLayout along axis {self.axis} with {self.num_slots} slots.'
    
    def apply(self, _volume:Volume, _parts:tuple[Part]):
        #
        # parts are arranged in increasing value along the axis
        # the assignment is greedy and respects the weights
        # if the sum of weights ls larger than 1, a warning is produced
        # and the result will be inconsistent

        logger = get_logger()
        logger.info(f'Applying layout {self} to volume {_volume} with {self.num_slots} slots.')
        # the initial available size is the whole volume
        # and its offset is the same as the base volume
        unallocated_volume = copy.deepcopy(_volume)
        for i,part in enumerate(_parts):
            if part is None:
                logger.info(f'Part {i} is empty.')
                continue
            # the alignment along the layout axis must be fixed to 'Left/Top/Right'
            piece = part.piece
            cons  = part.constraints
            orig_cons  = copy.deepcopy(cons)
            cons.alignment[self.axis] = LEFT # same as TOP and FRONT
            simple_layout(unallocated_volume,part)
            #
            # once laid out we tweak two things:
            # 1) the actual slot volume is reduced retroactively according to the piece volume
            #
            part.slot_volume = copy.deepcopy(unallocated_volume)
            margin_size = cons.margin.size()
            padding_size = cons.padding.size()
            # piece takes up all available space along axis, so piece volume and available are the same here
            # infer padded size from piece volume along axis
            part.available_volume.size.dim[self.axis] = part.piece_volume.size.dim[self.axis] 
            logger.info(f'Available volume (inferred back) {part.available_volume}')

            part.padded_volume.size.dim[self.axis] = part.available_volume.size.dim[self.axis] + margin_size.dim[self.axis]
            # infer slot size along axis from padded
            logger.info(f'Padded volume (inferred back) {part.padded_volume}')

            part.slot_volume.size.dim[self.axis] = \
                part.padded_volume.size.dim[self.axis] - padding_size.dim[self.axis]
            logger.info(f'Slot volume (inferred back) {part.slot_volume}')
            
            #
            # 2) we remove the slot volume from the beginning of the unallocated volume
            #    and move offset accordingly
            unallocated_volume.size.dim[self.axis]      -= part.slot_volume.size.dim[self.axis]
            unallocated_volume.offset.coords[self.axis] += part.slot_volume.size.dim[self.axis]

            #
            # if the part is a composite, lay it out
            #
            if isinstance(part.piece,CompositePiece):
                part.piece.apply_layout()

    def __tojson__(self):
        d = super().__tojson__()
        d['axis'] = self.axis
        return d
    
    def __fromjson__(d:dict):
        return StackLayout(d['slots'],d['axis'])

#--------------------------------------------------------------------


class CompositePiece(Piece):

    """
    a piece made up of other pieces
    sibling pieces are laid out according to a layout
    """
    def __init__(self, 
                 name:str, 
                 fixed_size:Size=Size(None,None,None),
                 layout:Layout=DefaultLayout(),
                 ):
        super().__init__(name=name,material=None,fixed_size=fixed_size)
        self.layout = layout
        self.parts = [None]*self.layout.slots()

    def translate(self,t:Vector):
        super().translate(self,t)
        for part in self.parts:
            if part is not None:
                piece = part.piece
                piece.volume.offset.translate(t)


    def add_part(self, piece:Piece, constraints:LayoutConstraints, position):
        if self.parts[position] is not None:
            get_logger().warning(f'There is already a piece at position {position}.')
        self.parts[position] = Part(piece,constraints)

    def apply_layout(self):
        self.layout.apply(self.volume,self.parts)

    def __str__(self):
        str = f'Composite piece with layout {self.layout} and {len(self.parts)} parts:\n'
        for i,p in enumerate(self.parts):
            str += f'{i})\n{p}'
        return str

    
    def description(self):
        return self.type() # not really needed because it is not a part or piece in itself

    def part_list(self):
        ret = list()
        for part in self.parts:
            if part is not None:
                pl = part.piece.part_list()
                ret.extend(pl)
        return ret

    def __tojson__(self):
        d = {}
        d['layout'] = self.layout.__tojson__()
        d['parts'] = list( p.__tojson__() for p in self.parts )
        return d
        