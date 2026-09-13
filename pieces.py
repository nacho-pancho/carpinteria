
from util import *
from core import *
from pieces import *
from materials import *

#--------------------------------------------------------------------

class Void(Piece):

    """ 
    a void piece is a piece that is not printed.
    """

    def __init__(self, 
                 name:str,
                 fixed_size:Size=Size(None,None,None)):
        super().__init__(name,
                         type='void', 
                         material=None, 
                         fixed_size=fixed_size)

    def part_list():
        return []


    def description(self)->str:
        """
        all voids are equal
        """
        return self.type()

    def from_dict(d:dict):
        obj = Void(d['name'])
        obj.constraints = LayoutConstraints.from_dict(d['constraints'])
        return obj


#--------------------------------------------------------------------

class Block(Piece):
    """
    A wooden block of arbitrary size
    """

    def __init__(self, 
                 name, 
                 material=PINE_WOOD_MATERIAL,
                 fixed_size:Size=Size(None,None,None)):
        super().__init__(name=name,
                         type='block',
                       material=material,
                       fixed_size=fixed_size)  
        self.screws = list()

    
    def part_description(self):
        dims = ['?','?','?']
        if self.size is not None:
            for i in range(3):
                if self.size[i] is not None:
                    dims[i] = self.size[i]
        w,d,h = dims        
        return f'block_of_{self.material.name}_{w}mm_x_{h}mm_x_{d}mm'

    def add_screw(self,position:Vector):
        pass

    def part_list(self):
        ret = list()
        ret.append(self.id())
        for s in self.screws():
            ret.append(s.id())

    def from_dict(d:dict):
        obj = Block(name=d['name'],
            material=Material.from_dict(d['material']))
        obj.constraints = LayoutConstraints.from_dict(d['constraints'])
        return obj
    
    def to_dict(self):
        d_base = super().to_dict()
        return d_base

 #--------------------------------------------------------------------

class Beam(Piece):
    """
    A wooden beam here is just a box made of wood with two dimensions
    that define the material in the materials list and a variable length
    the thicknesses are assigned as follows:
    if orientation is X, thickness 1 is about Y, and thickness 2 is about Z
    if orientation is Y, thickness 1 is about X, and thickness 2 is about Z
    if orietnation is Z, thickness 1 is about X, and thickness 2 is about Z
    that is, they fill in the dimensions that do not go along its direction,
    in the natural order.
    """

    def __init__(self, 
                 name, 
                 material, 
                 thickness1,
                 thickness2, 
                 orientation,
                 fixed_length:float=None):

        super().__init__(name=name,
                         type='beam',
                       material=material)  
        #
        # compute size constraints
        #
        if fixed_length is not None:
            min_length = fixed_length
            max_length = fixed_length

        if orientation == Z_COORD:
            self.constraints.min_size = Size(thickness1,thickness2,min_length)
            self.constraints.max_size = Size(thickness1,thickness2,max_length)

        elif orientation == Y_COORD:
            self.constraints.min_size = Size(thickness1,min_length,thickness2)
            self.constraints.max_size = Size(thickness1,min_length,thickness2)

        elif orientation == X_COORD:
            self.constraints.min_size = Size(min_length,thickness1,thickness2)
            self.constraints.max_size = Size(max_length,thickness1,thickness2)

        self.orientation = orientation
        self.thickness1= thickness1
        self.thickness2= thickness2
        self.screws = list()


    def part_description(self):
        length = self.size.dim[self.orientation]
        if length is None:
            length = '?'
        return f'{self.material.name}_{self.thickness1}mm_x_{self.thickness2}mm_x_{length}'

    def add_screw(self,position:Vector):
        pass

    def part_list(self):
        ret = list()
        ret.append(self.id())
        for s in self.screws():
            ret.append(s.id())

    def from_dict(d:dict):
        obj = Beam(
            name=d['name'],
            material=Material.from_dict(d['material']),
            thickness1=d['thickness1'],
            thickness2=d['thickness2'],
            orientation=d['orientation'])
        obj.constraints = LayoutConstraints.from_dict(d['constraints'])
        return obj
    

    def to_dict(self):
        d_base = super().to_dict()
        d_base['thickness1'] =  self.thickness1
        d_base['thickness2'] =  self.thickness2
        d_base['orientation'] =  self.orientation
        return d_base
    


#--------------------------------------------------------------------

class Sheet(Piece):
    """
    A sheet has a fixed thickness and variable width and height
    The thickness defines the fixed size along the face orientation
    """

    def __init__(self, 
                 name, 
                 material, 
                 thickness, 
                 face_orientation,
                 fixed_size:Size=Size(None,None,None),
                 ):
        super().__init__(name=name,
                         type='sheet',
                       material=material,
                       fixed_size=fixed_size)  
        self.face_orientation = face_orientation
        o = self.face_orientation
        self.constraints.min_size.dim[o] = thickness
        self.constraints.max_size.dim[o] = thickness
        self.thickness = thickness
        self.screws = list()

    
    def part_description(self):
        if self.face_orientation == X_COORD:
            dim1 = self.volume.size.dim[Z_COORD]
            dim2 = self.volume.size.dim[Y_COORD]
        elif self.face_orientation == Y_COORD:
            dim1 = self.volume.size.dim[X_COORD]
            dim2 = self.volume.size.dim[Z_COORD]
        else:
            dim1 = self.volume.size.dim[X_COORD]
            dim2 = self.volume.size.dim[Y_COORD]
        w,h = min(dim1,dim2),max(dim1,dim2)
        return f'{self.material.name}_{self.thickness}mm' # :TODO: complete this description with size

    def add_screw(self,position:Vector):
        pass

    def part_list(self):
        ret = list()
        ret.append(self.id())
        for s in self.screws():
            ret.append(s.id())

    def from_dict(d:dict):
        obj = Sheet(
            name=d['name'],
            material=Material.from_dict(d['material']),
            thickness=d['thickness'],
            face_orientation=d['face_orientation'])
        obj.constraints = LayoutConstraints.from_dict(d['constraints'])
        return obj

    
    def to_dict(self):
        d_base = super().to_dict()
        d_base['thickness'] =  self.thickness
        d_base['face_orientation'] =  self.face_orientation
        return d_base

#--------------------------------------------------------------------

class CoatingSpec(SizeModifier):
    """
    Coating on a board can be applied to any side
    it is identical to a SizeModifier in every aspect, so we reuse the class.
    a value of 0 means no coating on a side.
    a nonzero value specifies its thickness.
    """
    def __init__(self,_size=0):
        super().__init__('Coating',_size)

    def __str__(self)->str:
            return super().__str__()

    def to_dict(self):
        return super().to_dict()

    def from_dict(d):
        return CoatingSpec(_size=d)

#--------------------------------------------------------------------

class Board(Sheet):
    """
    A board is a sheet that may have a layer of coating on any of its two faces and any of its four sides.
    """
    def __init__(self, 
                 name, 
                 material, 
                 thickness, 
                 coating:CoatingSpec,
                 face_orientation,                  
                 fixed_size:Size=Size(None,None,None)):
        """
        Cretes a Board.
        This is identical to a Sheet, but adds 6 boolean parameters that specify whether
        there is coating on its top, bottom faces or any of its left, right, back and front sides.
        Here "front", "back", "left", "right", "bottom", "top" are to be imagined with the board
        laying horizontally on the floor, regardless of the actual orientation specified.
        """
        super().__init__(name=name,
                       material=material,
                       thickness=thickness,
                       fixed_size=fixed_size,
                       face_orientation=face_orientation)
        self.type = 'board' # overwrite 'sheet'
        self.coating = coating

    def part_description(self)->str:
        return super().part_description(self)

    def part_list(self):
        ret = list()
        ret.append(self.id())
        for s in self.screws():
            ret.append(s.id())

    def from_dict(d:dict):
        obj = Board(
            name=d['name'],
            material=Material.from_dict(d['material']),
            thickness=d['thickness'],
            face_orientation=d['face_orientation'],
            coating=CoatingSpec.from_dict(d['coating']))
        obj.constraints = LayoutConstraints.from_dict(d['constraints'])
        return obj

    def __str__(self):
        return  super().__str__() + f' coating {self.coating}'
    
    def to_dict(self):
        d_base = super().to_dict()
        d_base['coating'] = self.coating.to_dict()
        return d_base
    
#--------------------------------------------------------------------

class DrawerGuide(Piece):
    """
    drawer guide. stretches along positive Y  (to the back)
    """
    DEFAULT_THICKNESS = 13 # they are about 13mm thick
    DEFAULT_WIDTH = 40 # good ones about 4cm
    def __init__(self, 
                 name:str, 
                 length:float, 
                 orientation:int, 
                 thickness=DEFAULT_THICKNESS, 
                 width=DEFAULT_WIDTH):

        super().__init__(name=name,
                         type='guide',
                         material=GUIDE_MATERIAL)

        self.orientation = orientation
        self.length = length
        self.thickness = thickness
        self.width = width
        #
        # size is 100% fixed
        #
        if self.orientation == Z_COORD: # weird for a guide but ok..., assume it is attached to a frontal plane
            self.constraints.min_size = Size(self.thickness,self.width,self.length)
            self.constraints.max_size = Size(self.thickness,self.width,self.length)
        elif self.orientation == X_COORD: # a little less weird, assume attached to a vertical plane
            self.constraints.min_size = Size(self.length,self.thickness,self.width)
            self.constraints.max_size = Size(self.length,self.thickness,self.width)
        elif self.orientation == Y_COORD: # most common, assume it is attached to a vertical plane
            self.constraints.min_size = Size(self.thickness,self.length,self.width)
            self.constraints.max_size = Size(self.thickness,self.length,self.width)
        else:
            raise ValueError(f'Invalid guide orientation {self.orientation}.')


    def part_description(self)->str:
        return f'{self.type()}_{self.length}mm'


    def part_list(self):
        ret = list()
        ret.append(self.id())


#--------------------------------------------------------------------

class NailLike(Piece):
    """
    A little thing with a beam and a head, like a screw or a nail
    """

    def __init__(self, name:str, 
                 type:str, 
                 material:Material, 
                 caliber:int,
                 head_width:int, 
                 head_height:int,
                 length:int, 
                 direction:int):
        self.caliber = caliber
        self.length = length
        self.direction = direction
        self.head_width = head_width
        self.head_height = head_height

        if self.direction == BOTTOM_TO_TOP or self.direction == TOP_TO_BOTTOM:        
            fixed_size = Size(self.head_width,self.head_width,self.length)
        elif self.direction == LEFT_TO_RIGHT or self.direction == RIGHT_TO_LEFT:        
            fixed_size = Size(self.length, self.head_width,self.head_width)
        elif self.direction == FRONT_TO_BACK or self.direction == BACK_TO_FRONT:        
            fixed_size = Size(self.head_width,self.length,self.head_width)
        else:
             raise ValueError(f'Invalid direction {self.direction}.')
        super().__init__(name=name, type=type, material=material,fixed_size=fixed_size)
    
    def part_list(self):
        ret = list()
        ret.append(self.id())

    def to_dict(self):
        d = super().to_dict()
        d['caliber'] = self.caliber
        d['direction'] = self.direction
        d['length'] = self.length
        d['head_width'] = self.head_width
        d['head_height'] = self.head_height
        return d


#--------------------------------------------------------------------

class Screw(NailLike):
    """
    a screw. 
    """

    def __init__(self, name, material, caliber, length, direction):
        super().__init__(name=name,
                         type='screw',
                         material=material,
                         caliber=caliber,
                         length=length,
                         head_height=1,
                         head_width=2*caliber,
                         direction=direction)

    def part_description(self)->str:
        return f'{self.type()}_{self.caliber}mm_x_{self.length}mm'


    def from_dict(d:dict):
        return Screw(name=d['name'],
                     material=Material.from_dict(d['material']),
                     caliber=d['caliber'],
                     length=d['length'],
                     direction=d['direction'])

#--------------------------------------------------------------------

class Nail(NailLike):
    """
    A nail.
    """

    def __init__(self,name, caliber, length, direction):
        super().__init__(name=name,
                         type='nail',
                         material=NAIL_MATERIAL,
                         caliber=caliber,
                         length=length,
                         head_height=1,
                         head_width=2*caliber,
                         direction=direction)


    def from_dict(d:dict):
        return Nail(name=d['name'],
                     caliber=d['caliber'],
                     length=d['length'],
                     direction=d['direction'])

    def part_description(self)->str:
        return f'{self.type()}_{self.caliber}mm_x_{self.length}mm'

#--------------------------------------------------------------------

class Dowel(NailLike):
    """
    Dowel or Dowel pin in English
    Tarugo in spanish (only way I can remember this)
    Small peg of wood used to join two boards or something like that
    """

    def __init__(self,name, length, direction):
        super().__init__(name=name,
                         type='dowel',
                         material=DOWEL_MATERIAL,
                         caliber=6,
                         length=length,
                         head_height=0,
                         head_width=6,
                         direction=direction)


    def part_description(self)->str:
        return f'{self.type()}_{self.length}mm'

    def from_dict(d:dict):
        return Dowel(name=d['name'],
                     length=d['length'],
                     direction=d['direction'])


#--------------------------------------------------------------------

class CornerBrace(Piece):
    """
    prism shaped plastic piece for 90 degrees joints from within; 
    useful for table surfaces and drawer fronts
    """
    def __init__(self,name, orientation):
        if orientation == X_COORD:
            size = Size(40,20,20)
        elif orientation == Y_COORD:
            size = Size(20,40,20)
        elif orientation == Z_COORD:
            size = Size(20,20,40)
        super().__init__(name=name,
                         type='corner',
                         material=CORNER_MATERIAL,
                         fixed_size=size)


    def part_description(self):
        return self.type()

    def from_dict(d:dict):
        return CornerBrace(name=d['name'],
                     direction=d['direction'])

#--------------------------------------------------------------------

PIECE_TYPES = {
    'composite': CompositePiece,
    'void': Void, 
    'block': Block,
    'beam': Beam,
    'sheet': Sheet,
    'board': Board,
    'nail': Nail,
    'dowel': Dowel,
    'screw': Screw,
    'guide': DrawerGuide,
    'corner': CornerBrace
}
