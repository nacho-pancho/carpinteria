#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#
# relative position of piece within a layout (used mostly with default Layout)
# 
from dataclasses import dataclass


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

class Layout():
    
    def __init__(self, width:float, height:float, depth:float):
        self.width = width
        self.height = height
        self.depth = depth

    def apply(self, volume: float):
        pass

class DefaultLayout(Layout):

    def __init__(self):
        pass

    def apply(self, volume: float):
        pass

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
        self.holes = list()


    def translate(self,dx:float,dy:float,dz:float):
        for p in self.parts:
            p.translate(dx,dy,dz)


    def rotate(self,rx:float,ry:float,rz:float):
        for p in self.parts:
            p.rotate(rx,ry,rz)

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


class Void(Piece):

    """ 
    a void piece is a piece that is not printed.
    """

    def __init__(self, size:tuple[float],
                 min_size:tuple[float]=None, 
                 max_size:tuple[float]=None
                 ):
        super().__init__('void', 
                         None, 
                         size=size, 
                         min_size=min_size, 
                         max_size=max_size)
    
class Volume():

    def __init__(self, width:float, height:float, depth:float, position: tuple[float]):
        self.width = width
        self.height = height
        self.depth = depth
        self.position = position
        self.margin = Margin()
        self.padding = Padding()
        self.depth_alignment = CENTER
        self.horizontal_alignment = CENTER
        self.vertical_alignment = CENTER     
        self.pieces = list()
        self.layout = DefaultLayout(width, height, depth)
        self.weight = tuple[float] 

    def add_piece(self, piece:Piece, position=None):
        self.pieces.append((piece, position))
        self.layout.apply(piece)



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

