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
import typing
from dataclasses import dataclass
import numpy as np
import math
import logging

def get_logger():
    if get_logger._logger is None:
        logging.basicConfig(level=logging.INFO)
        get_logger._logger = logging.getLogger()
    return get_logger._logger
get_logger._logger = None

def set_logging_level(level):
    get_logger().setLevel(level)

def debug_mode():
    return get_logger().level == logging.DEBUG
        
BACK  = 'back'
FRONT = 'front'
LEFT  = 'left'
RIGHT = 'right'
TOP   = 'top'
BOTTOM = 'bottom'
CENTER = 'center'

X_COORD = 0
Y_COORD = 1
Z_COORD = 2

INFINITY = 1000000000 # 1000km is quite large for a furniture
#
# ==========================================================
# Basic types
# ==========================================================
#

class Vector():

    def __init__(self,x=0,y=0,z=0):
        self.coords = [x,y,z]

    def __getitem__(self,i):
        return self.coords[i]

    def add(self,dv:Vector):
        self.coords[X_COORD] += dv[X_COORD]
        self.coords[Y_COORD] += dv[Y_COORD]
        self.coords[Z_COORD] += dv[Z_COORD]

    def translate(self,dv:Vector):
        return self.add(dv)

    def rotate(self,axis:int, angle:float):
        x,y,z = self.coords[:]
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
        else:
            raise ValueError(f'Rotation axis can be 0, 1 or 2. {axis} given.')
        self.coords = [new_x,new_y,new_z]

    def __str__(self):
        return self.coords.__str__()
    
# conceptully different but same thing inside
type Point = Vector


@dataclass
class SizeModifier():
    """
    reserves space within a volume 
    """
 
    def __init__(self,_type,_size=None):

        self.values = [[0,0],[0,0],[0,0]]
        self.type = _type
        if _size is None:
            return
        #
        # a million ways to define a margin
        # - a single value: repeat this value on all side
        # - 3 scalars: same value o both sides along each direction
        # - 6 scalars: a particular value for each direction and side
        # - 3 tuples of 2: same as 6 but overly complicated
        #
        if type(_size) == tuple:
            if len(_size) == 6:
                for i in range(3):
                    self.values[i] = _size[2*i:2*(i+1)]
            elif len(_size) == 3:
                for i in range(3):
                    if type(_size[i]) == tuple:
                        if len(_size[i]) == 2:
                            self.values[2*i] = self.values[2*i+1] = _size[i]
                        else:
                            raise ValueError(f'{_type} argument must be either a scalar, a tuple of 3, a tuple of 6, or a tuple of 3 tuples of 2')                            
            else:
                raise ValueError(f'{_type} argument must be either a scalar, a tuple of 3, a tuple of 6, or a tuple of 3 tuples of 2')
        else:
            for i in range(3):
                for j in range(2):
                    self.values[i][j] = _size

    def left(self):
        return self.values[X_COORD][0]

    def right(self):
        return self.values[X_COORD][1]

    def top(self):
        return self.values[Z_COORD][0]

    def bottom(self):
        return self.values[Z_COORD][1]

    def front(self):
        return self.values[Y_COORD][0]

    def back(self):
        return self.values[Y_COORD][1]
    
    def __getitem__(self,i):
        return self.values[i]

    def __str__(self):
        return f'{self.type} (left:{self.left()} right:{self.right()} top:{self.top()} bottom:{self.bottom()} front:{self.front()} back: {self.back()})'


class Padding(SizeModifier):
    def __init__(self,_size=0):
        super().__init__('Padding',_size)


    def __str__(self):
        return super().__str__()
    
class Margin(SizeModifier):
    def __init__(self,_size=0):
        super().__init__('Margin',_size)

    def __str__(self):
            return super().__str__()

    
type Weight = Vector

class Size():

    def __init__(self,sx:float=0,sy:float=0,sz:float=0):
        self.dim = [sx,sy,sz]


    def width(self): 
        return self.dim[X_COORD]


    def height(self):
        return self.dim[Z_COORD]


    def depth(self):
        return self.dim[Y_COORD]

    
    def grow(self,size:Size):
        self.dim[X_COORD] += size.dim[X_COORD]
        self.dim[Y_COORD] += size.dim[Y_COORD]
        self.dim[Z_COORD] += size.dim[Z_COORD]

    def shrink(self,size:Size):
        self.dim[X_COORD] -= size.dim[X_COORD]
        self.dim[Y_COORD] -= size.dim[Y_COORD]
        self.dim[Z_COORD] -= size.dim[Z_COORD]


    def __getitem__(self,i):
        return self.dim[i]

    def __str__(self):
        return self.dim.__str__()

    
class LayoutConstraints():
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
        self.piece = None

    def __str__(self):
        return f'''LayoutConstraints:\
 {self.padding}\
 {self.margin} weight {self.weight}\
 alignment {self.alignment}'''
    
class Layout():
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

def effective_dim(_min:float, _max:float, _weight:float, _available:float):
    """
    determine the value of a dimension taking into account the available magnitude hard and soft constraints
    * If a fixed value is specified, then just return this value.
    * The desired size is _weight*_available
    * If the minimum is not specified, it is assumed to be 0
    * If the maximum is not specified, it is assumed to be infinite
    * If the available size is smaller than the minimum, return the minimum **but with a warning**
    * If the desired size is larger than the maximum, return the maximum
    * If the desired size is smaller than the minimum, return the minimum
    """
    logger = get_logger()
    logger.debug(f'effective_dim: min {_min} _max {_max} _weight {_weight} _available {_available}')
    _desired = _weight * _available
    logger.debug(f'_desired {_desired}')
    #
    # the weight only applies if the desired size falls within [_min,_max]
    # the degenerate case is when _min > _available
    #
    if _min > _available:
        print(f'WARNING: minimum size {_min} does not fit in available space {_available}')
        _weight = 1 # force weight to be 1 in this case

    _effective = max(_min,min(_max,_desired))
    logger.debug(f'effective {_effective}')
    return _effective

def effective_size(_min,_max,_weight,_available):
    return Size(*[effective_dim(_min[i],_max[i],_weight[i],_available[i]) for i in range(3)])


@dataclass
class Volume():
    """
    A rectangular region in space
    """
    size:Size
    offset:Vector # lower left front corner

    def __init__(self,size:Size=Size(),off:Vector=Vector()):
        self.size = size
        self.offset = off


    def add_padding(self,p:Padding):
        """
        padding enlarges the volume and shifts the offset outwards
        """
        for i in range(3):
            self.size.dim[i] += p[i][1] + p[i][0]
            self.offset.coords[i] -= p[i][0]

    def add_margin(self,m:Margin):
        """
        margin reduces the volume and shifts the offset to the interior
        """
        for i in range(3):
            self.size.dim[i] -= m[i][1] + m[i][0]
            self.offset.coords[i] += m[i][0]


    def __str__(self):
        return f'Volume of size {self.size} at offset {self.offset}'

def add_padding(v:Volume,p:Padding):
    ret = copy.deepcopy(v)
    ret.add_padding(p)
    return ret

def add_margin(v:Volume,m:Margin):
    ret = copy.deepcopy(v)
    ret.add_margin(m)
    return ret


class Part():
    """
    part of a multi-piece object
    """

    def __init__(self,piece:Piece,constraints:LayoutConstraints):
        self.base_volume = Volume()
        self.padded_volume = Volume()
        self.available_volume = Volume()
        self.piece_volume = Volume()
        self.piece = piece
        self.constraints = constraints

    def __str__(self):
        return f'Part:\n\t{self.piece}\n\t{self.constraints}'

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

        part = _parts[0]
        piece = part.piece
        cons  = part.constraints
        logger.info(f'laying out {piece}\nwith {cons}')
        #
        # there are three volumes:
        # the base volume
        # the padded volume, which results from the base volume being grown
        # the available volume, which results from the padded volume being reduced by the margins
        #
        # we keep track of them all
        part.base_volume = copy.deepcopy(_volume)
        logger.info(f'Base volume {part.base_volume}')
        part.padded_volume = add_padding(part.base_volume,cons.padding)
        logger.info(f'Padded volume {part.padded_volume}')
        part.available_volume = add_margin(part.padded_volume,cons.margin)
        logger.info(f'Available volume {part.available_volume}')

        # now we have the available volume
        # we take into account the piece's own constraints (min and max size)
        # to determine its final size
        piece_size = effective_size(piece.min_size, 
                                piece.max_size, 
                                cons.weight,
                                part.available_volume.size)
        part.piece_volume = Volume(piece_size,copy.deepcopy(part.available_volume.offset))

        logger.info(f'Piece volume {part.piece_volume} (prior to alignment)')
        for i in range(3):
            delta = (part.available_volume.size.dim[i] - part.piece_volume.size.dim[i])
            logger.info(f'Excess volume at dimension {i} is {delta}')
            if cons.alignment[i] == CENTER:
                logger.info(f'Center alignment implies displacement by {delta/2}.')
                part.piece_volume.offset.coords[i] += delta / 2
            elif cons.alignment[i] == RIGHT or cons.alignment == BACK or cons.alignment == TOP:
                logger.info(f'right/top/back alignment implies displacement by {delta}.')
                part.piece_volume.offset.coords[i] += delta
        #
        # the final part is the placement of the piece if the piece
        # is smaller than the effective volume, it needs to be arranged
        # according to the alignment
        # 
        # put the piece according to the constraints
        piece.volume = copy.deepcopy(part.piece_volume)
        logger.info(f'Final volume {piece.volume} (after alignment)')


    def slots(self):
        return 1

    def __str__(self):
        return 'Default layout'
    

class ZStackLayout(Layout): 
    """ 
    splits a volume into a vertical pile of slices along the Z axis
    """

    def __init__(self,num_slots:int):
        self.num_slots = num_slots

    def apply(self, volume: float):
        pass

    def slots(self):
        return self.num_slots


class XStackLayout(Layout): 
    """ 
    splits a volume horizontally in blocks along the X axis
    """
    
    def __init__(self,num_slots:int):
        self.num_slots = num_slots

    def apply(self, volume: float):
        pass

    def slots(self):
        return self.num_slots

class YStackLayout(Layout): 
    """ 
    splits a volume horizontally in blocks along the Y axis
    """
    
    def __init__(self,num_slots:int):
        self.num_slots = num_slots

    def apply(self, volume: float):
        pass

    def slots(self):
        return self.num_slots


class Piece():

    def __init__(self, 
                 name:str, 
                 material:str,
                 size:Size=None,
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 color:str=None
                 ):
        self.name = name
        self.color = color
        self.material = material
        self.min_size = min_size 
        self.max_size = max_size
        self.volume = Volume(size,Vector())

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


class CompositePiece(Piece):

    """
    a piece made up of other pieces
    sibling pieces are laid out according to a layout
    """
    def __init__(self, 
                 name:str, 
                 size:tuple[float]=None,
                 color:str=None
                 ):
        super().__init__(name,'composite',size,color)
        self.layout = DefaultLayout()
        self.parts = [None]*self.layout.slots()

    def translate(self,t:Vector):
        super().translate(self,t)
        for p in self.parts:
            if p is not None:
                p.offset.translate(t)


    def add_piece(self, piece:Piece, constraints:LayoutConstraints, position=0):
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


class Void(Piece):

    """ 
    a void piece is a piece that is not printed.
    """

    def __init__(self, size:Size):
        super().__init__('void', 
                         'nothing', 
                         size=size)


class Sheet(Piece):
    """
    A sheet has a fixed thickness and variable width and height 
    It can be created so that it runs along the X-Y axis (frontal), along the X-Z axis 
    """
    ORIENT_LATERAL = 'lateral' # Y-Z,  width goes to the back, height goes up, thickness is in X
    ORIENT_FRONTAL = 'frontal' # X-Z, width goes sideways, height goes up, thickness in Y
    ORIENT_HORIZONTAL = 'horizontal' # width goes sideways, height goes back, thickness in Z

    def __init__(self, name, material, thickness, orientation, color=None):
        if min_size is None:
            min_size = [None,None,None]
        if max_size is None:
            max_size = [None,None,None]
        if orientation == Sheet.ORIENT_LATERAL:
            if min_size[X_COORD] is not None:
                print('Warning: min_size specified for X in lateral sheet is overwritten by thicnkess.')
            min_size[X_COORD] = thickness
            if max_size[X_COORD] is not None:
                print('Warning: max_size specified for X in lateral sheet is overwritten by thicnkess.')
            max_size[X_COORD] = thickness
        elif orientation == Sheet.ORIENT_FRONTAL:
            if min_size[Y_COORD] is not None:
                print('Warning: min_size specified for Y in  lateral sheet is overwritten by thicnkess.')
            min_size[Y_COORD] = thickness
            if max_size[Y_COORD] is not None:
                print('Warning: max_size specified for Y in lateral sheet is overwritten by thicnkess.')
            max_size[Y_COORD] = thickness
        elif orientation == Sheet.ORIENT_HORIZONTAL:
            if min_size[Z_COORD] is not None:
                print('Warning: min_size specified for Z in horizontal sheet is overwritten by thickness.')
            min_size[Z_COORD] = thickness
            if max_size[Z_COORD] is not None:
                print('Warning: max_size specified for Z in horixontal sheet is overwritten by thickness.')
            max_size[Z_COORD] = thickness
        super.__init__(name,material,min_size,max_size,color)
        self.orientation = orientation


class Board(Sheet):
    """
    A board is a sheet that may have a layer of coating on any of its two faces and any of its four sides.
    """
    def __init__(self, 
                 name, 
                 material, 
                 thickness, 
                 orientation, 
                 min_size=None, 
                 max_size=None, 
                 color=None, 
                 top=False, bottom=False, left=False, right=False, back=False, front=False):
        """
        Cretes a Board.
        This is identical to a Sheet, but adds 6 boolean parameters that specify whether
        there is coating on its top, bottom faces or any of its left, right, back and front sides.
        Here "front", "back", "left", "right", "bottom", "top" are to be imagined with the board
        laying horizontally on the floor, regardless of the actual orientation specified.
        """
        super.__init__(name,material,thickness,orientation,max_size,min_size,color)
        self.coating_top = top
        self.coating_bottom = bottom
        self.coating_back = back
        self.coating_front = front
        self.coating_left = left
        self.coating_rigth = right

class Screw(Piece):
    """
    a screw. Appears vertically by default
    """
    FLAT_HEAD = 'flat'
    WOOD = 'wood'

    def __init__(self,name, caliber,length, direction, _type):
        self.type = _type
        self.caliber = caliber
        self.length = length
        self.direction = direction
        if self.type == Screw.FLAT_HEAD:
            color = (0.7,0.8,0.9)
            head_radius = caliber * 2
        elif self.type == Screw.WOOD:
            color = (0.8,0.7,0.6)
            head_radius = caliber
        material = f'screw_{_type}_{caliber}mmx{length}mm'
        min_size = (2*head_radius,2*head_radius,length)
        max_size = min_size
        size = min_size   
        super.__init__(name,material,size,min_size,max_size,color)

class DrawerGuide(Piece):
    """
    drawer guide. stretches along positive Y  (to the back)
    """
    DEFAULT_THICKNESS = 13 # they are about 13mm thick
    DEFAULT_WIDTH = 40 # good ones about 4cm
    def __init__(self,name, length, orientation, thickness=DEFAULT_THICKNESS, width=DEFAULT_WIDTH):
        self.orientation = orientation
        self.length = length
        self.thickness = thickness
        color = (0.7,0.8,0.9)
        material = f'guide_{length}mm'
        min_size = (self.thickness,self.width,length)
        max_size = min_size
        size = min_size   
        super.__init__(name,material,size,min_size,max_size,color)
