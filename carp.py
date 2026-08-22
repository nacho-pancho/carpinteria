#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#
# relative position of piece within a layout (used mostly with default Layout)
# 
from dataclasses import dataclass
import numpy as np
import math

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


@dataclass
class Margin():
    """
    reserves space within a volume 
    """
    left: float
    right: float
    top: float
    bottom: float
    back: float
    front: float

    def __init__(self,size=0):
        left = size
        right = size
        top = size
        bottom = size
        back = size
        front = size

@dataclass
class Padding():
    """
    extends a volume outside its base size
    """
    left: float
    right: float
    top: float
    bottom: float
    back: float
    front: float

    def __init__(self,size=0):
        left = size
        right = size
        top = size
        bottom = size
        back = size
        front = size

class Volume():
    """
    place where pieces are put
    """
    width: float
    height: float
    depth: float

    def __init__(self,size=0):
        self.width = size
        self.height = size
        self.depth = size
        self.padding = Padding()
        self.margin = Margin()
        self.weight = [0,0,0]
        self.depth_alignment = CENTER
        self.horizontal_alignment = CENTER
        self.vertical_alignment = CENTER
        self.piece = None

class Layout():
    
    def __init__(self, width:float, height:float, depth:float):
        self.width = width
        self.height = height
        self.depth = depth

    def apply(self, volume: float):
        pass

    def places(self):
        return 1

def effective_size(_min, _max, _fixed, _available):
    if _fixed is not None:
        return _fixed
    if _min is None:
        _min = 0
    if _max is None:
        _max = _available
    if _min < _available:
        return min(_max,_available) # ok, we take all that we can
    else:
        print(f'WARNING: minimum size {_min} does not fit in available space {_available}')
        return _min


class DefaultLayout(Layout):

    def __init__(self):
        pass

    def apply(self, composite_piece: CompositePiece):
        pass

    def places(self):
        return 1

class ZStackLayout(Layout): 
    """ 
    splits a volume into a vertical pile of slices along the Z axis
    """

    def __init__(self):
        pass

    def apply(self, volume: float):
        pass


class XStackLayout(Layout): 
    """ 
    splits a volume horizontally in blocks along the X axis
    """
    
    def __init__(self):
        pass

    def apply(self, volume: float):
        pass

class YStackLayout(Layout): 
    """ 
    splits a volume horizontally in blocks along the Y axis
    """
    
    def __init__(self):
        pass

    def apply(self, volume: float):
        pass


class Piece():

    def __init__(self, 
                 name:str, 
                 material:str,
                 size:tuple[float]=None,
                 min_size:tuple[float]=None, 
                 max_size:tuple[float]=None,
                 color:str=None
                 ):
        self.name = name
        self.color = color
        self.material = material
        self.parts = list()
        self.size = size
        self.min_size = min_size
        self.max_size = max_size
        self.offset = [0,0,0]

    def translate(self,t:tuple[float]):
        self.offset[0] += t[0]
        self.offset[1] += t[1]
        self.offset[2] += t[2]

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
                 material:str,
                 size:tuple[float]=None,
                 min_size:tuple[float]=None, 
                 max_size:tuple[float]=None,
                 color:str=None
                 ):
        super().__init__(name,'composite',size,min_size,max_size,color)
        self.layout = DefaultLayout()
        vol = Volume()
        self.volumes = [vol]*self.layout.places()


    def translate(self,t:tuple[float]):
        super().translate(self,t)
        for p in self.parts:
            if p is not None:
                p.translate(t)


    def rotate(self,axis:float, angle:float):
        super().rotate(self,axis,angle)
        for p in self.parts:
            if p is not None:
                p.rotate(axis, angle)


    def add_piece(self, piece:Piece, position=0):
        self.volumes[position].piece = piece


    def apply_layout(self):
        pass


class Void(Piece):

    """ 
    a void piece is a piece that is not printed.
    """

    def __init__(self, size:tuple[float]=None,
                 min_size:tuple[float]=None, 
                 max_size:tuple[float]=None
                 ):
        super().__init__('void', 
                         None, 
                         size=size, 
                         min_size=min_size, 
                         max_size=max_size)
    

class Sheet(Piece):
    """
    A sheet has a fixed thickness and variable width and height 
    It can be created so that it runs along the X-Y axis (frontal), along the X-Z axis 
    """
    ORIENT_LATERAL = 'lateral' # Y-Z,  width goes to the back, height goes up, thickness is in X
    ORIENT_FRONTAL = 'frontal' # X-Z, width goes sideways, height goes up, thickness in Y
    ORIENT_HORIZONTAL = 'horizontal' # width goes sideways, height goes back, thickness in Z

    def __init__(self, name, material, thickness, orientation, min_size=None, max_size=None, color=None):
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
