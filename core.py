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
                 type:str,
                 material:Material,
                 fixed_size:Size=Size(None,None,None),
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 ):
        self.name = name
        self.type = type
        self.material = material
        self.min_size = copy.deepcopy(min_size) 
        self.max_size = copy.deepcopy(max_size)
        self.volume = Volume(copy.deepcopy(fixed_size),Vector())
        # fixed_size overrides min_size and max_size 
        for i in range(3):
            if fixed_size[i] is not None:
                self.min_size.dim[i] = self.max_size.dim[i] = fixed_size[i]
            # fixed size may be implicit if min = max
            # in either case, the volume is fixed in that dimension
            if self.min_size.dim[i] == self.max_size.dim[i]:
                self.volume.size.dim[i] = self.min_size.dim[i]


    def __str__(self):
        return f'''Piece {self.name} of type {self.type} made of {self.material}\
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


    def to_dict(self)->dict:
        d = {}
        d["type"] = self.type
        d["name"] = self.name
        d["material"] =  self.material.to_dict()
        d["min_size"] =  self.min_size.to_dict()
        d["max_size"] =  self.max_size.to_dict()
        d["volume"]   =    self.volume.to_dict() 
        return d

    # should never be called
    # just to mark the 'idea' of having this class 
    # method for each piece so that we can do Class.from_dict(d)
    def from_dict(d:dict)->Piece:
        raise NotImplementedError()


    

#--------------------------------------------------------------------

class LayoutConstraints(JSONable):
    """
    Contains some information about how
    to put a piece inside of it, such as margins to the sides, padding, alignment in all directions.
    For some layout methods it also contains a 'weight' which is between 0 and 1. If space needs to 
    be shared between objects, then this specifies how much of the space should be taken, if possible.
    Weight is a soft constraint; hard constraints such as minimum and fixed sizes prevail, if defined.
    """

    def __init__(self,
                 padding:Padding=Padding(),
                 margin:Margin=Margin(),
                 weight:list[float]=[1,1,1],
                 alignment:list[str]=[CENTER,CENTER,CENTER]):
        self.padding = padding
        self.margin = margin
        self.weight = weight
        self.alignment = alignment

    def __str__(self):
        return f'''LayoutConstraints:\
 {self.padding}\
 {self.margin} weight {self.weight}\
 alignment {self.alignment}'''

    def to_dict(self):
        return {'padding': self.padding.to_dict(self),
                'margin': self.margin.to_dict(self),
                'weight': self.weight,
                'alignment': self.alignment}

    def from_dict(d:dict):
        padding = Padding.from_dict(d['padding'])
        margin = Margin.from_dict(d['margin'])
        weight = d['weight']
        alignment = d['alignment']
        return LayoutConstraints(padding=padding,
                                 margin=margin,
                                 weight=weight,
                                 alignment=alignment)


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

    def to_dict(self)->dict:
        d = {}
        d['piece'] = self.piece.__json__(),
        d['constraints'] = self.constraints.__json__()
        return d

#--------------------------------------------------------------------

class Layout(JSONable):
    """
    Strategy or method by which pieces are put inside a composite piece.
    This is a typical concept in UI design. I'm copying it here.
    """
    def __init__(self,type):
        self._type = type

    def apply(self, composite: CompositePiece):
        return NotImplementedError()

    def slots(self):
        return NotImplementedError()

    def to_dict(self):
        return {'type': self.type(), 'slots': self.slots() }

    def type(self):
        return self.type
 

#--------------------------------------------------------------------


class CompositePiece(Piece):

    """
    a piece made up of other pieces
    sibling pieces are laid out according to a layout
    """
    def __init__(self, 
                 name:str, 
                 fixed_size:Size=Size(None,None,None),
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 layout:Layout=None):
        super().__init__(name=name,
                         type='composite',
                         material=None,
                         fixed_size=fixed_size,
                         min_size=min_size,
                         max_size=max_size)
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
        if self.layout is None:
            raise ValueError(f'Layout not defined.')
        self.layout.apply(self.volume,self.parts)

    def __str__(self):
        str = f'Composite piece with layout {self.layout} and {len(self.parts)} parts:\n'
        for i,p in enumerate(self.parts):
            str += f'{i})\n{p}'
        return str

    
    def part_description(self):
        return f'composite with {len(self.parts)} parts and layout {self.layout}'
    
    def part_list(self):
        ret = list()
        for part in self.parts:
            if part is not None:
                pl = part.piece.part_list()
                ret.extend(pl)
        return ret


    def type(self):
        return 'composite'


    def to_dict(self):
        d = {}
        d['layout'] = self.layout.to_dict()
        d['parts'] = list( p.to_dict() for p in self.parts )
        return d


class Project(JSONable):
    def __init__(self,name="no name",version="no version",date="no date",author="no one",description='no description'):
        self.name = name
        self.version = version
        self.date = date
        self.author = author
        self.description = description
        self.pieces = list()

    def add_piece(self,p:Piece):
        self.pieces.append(p)

    def __str__(self):
        str = f'Project: {self.name} v{self.version}, date {self.date}, author {self.author}.\n'
        str += f'Description:{self.description}\n'
        str += 'Parts:\n'
        for p in self.pieces:
            str += p.__str__() + '\n'
        return str
    
    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['version'] = self.version
        d['date'] = self.date
        d['author'] = self.author
        d['description'] = self.description
        d['pieces'] = list( p.to_dict() for p in self.pieces )
        return d
