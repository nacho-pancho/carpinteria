
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
                 fixed_size:Size=Size(None,None,None),
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 ):
        super().__init__(name,
                         type='void', 
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
        return self.type()

    def from_dict(d:dict):
        min_size = Size.from_dict(d['min_size'])
        max_size = Size.from_dict(d['max_size'])
        obj = Void(d['name'],min_size=min_size, max_size=max_size)
        obj.volume = Volume.from_dict(d['volume'])
        return obj
    
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
                 length:float=None,
                 min_length:float=0,
                 max_length:float=INFINITY
                 ):

        if orientation == Z_COORD:
            min_size = Size(thickness1,thickness2,min_length)
            max_size = Size(thickness1,thickness2,max_length)

        elif orientation == Y_COORD:
            min_size = Size(thickness1,min_length,thickness2)
            max_size = Size(thickness1,min_length,thickness2)

        elif orientation == X_COORD:
            min_size = Size(min_length,thickness1,thickness2)
            max_size = Size(max_length,thickness1,thickness2)

        if length is not None:
            min_size.dim[orientation] = length
            max_size.dim[orientation] = length
            min_length = length
            max_length = length

        super().__init__(name=name,
                         type='beam',
                       material=material,
                       min_size=min_size,
                       max_size=max_size)  
        self.orientation = orientation
        self.thickness1= thickness1
        self.thickness2= thickness2
        self.min_length = min_length
        self.max_length = max_length
        self.length = length
        self.screws = list()


    def id(self):
        if self.orientation == X_COORD:
            dim1 = self.volume.size.dim[Z_COORD]
            dim2 = self.volume.size.dim[Y_COORD]
        elif self.orientation == Y_COORD:
            dim1 = self.volume.size.dim[X_COORD]
            dim2 = self.volume.size.dim[Z_COORD]
        else:
            dim1 = self.volume.size.dim[X_COORD]
            dim2 = self.volume.size.dim[Y_COORD]
        w,h = min(dim1,dim2),max(dim1,dim2)
        return f'{self.material.name}_{self.thickness}mm_x_{self.thickness}mm'

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
            orientation=d['orientation'],
            length=d['length'],
            min_length=d['min_length'],
            max_length=d['max_length'])
        obj.volume = Volume.from_dict(d['volume'])
        return obj
    

    def to_dict(self):
        d_base = super().to_dict()
        d_base['thickness1'] =  self.thickness1
        d_base['thickness2'] =  self.thickness2
        d_base['length'] =  self.length
        d_base['orientation'] =  self.orientation
        d_base['min_length'] =  self.min_length
        d_base['max_length'] =  self.max_length
        return d_base
    

#--------------------------------------------------------------------

class Block(Piece):
    """
    A wooden block of arbitrary size
    """

    def __init__(self, 
                 name, 
                 material=PINE_WOOD_MATERIAL,
                fixed_size:Size=Size(None,None,None),
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 ):
        super().__init__(name=name,
                         type='block',
                       material=material,
                       fixed_size=fixed_size,
                       min_size=min_size,
                       max_size=max_size)  
        self.screws = list()

    
    def part_description(self):
        dims = ['?','?','?']
        if self.volume is not None:
            for i in range(3):
                if self.volume.size[i] is not None:
                    dims[i] = self.volume.size[i]
        w,d,h = dims        
        return f'block_of_{self.material.name}_{w}_x_{h}_x_{d}_mm'

    def add_screw(self,position:Vector):
        pass

    def part_list(self):
        ret = list()
        ret.append(self.id())
        for s in self.screws():
            ret.append(s.id())

    def from_dict(d:dict):
        obj = Block(
            name=d['name'],
            min_size=Size.from_dict(d['min_size']),
            max_size=Size.from_dict(d['max_size']),
            material=Material.from_dict(d['material'])
            )
        obj.volume = Volume.from_dict(d['volume'])
        return obj
    
    def to_dict(self):
        d_base = super().to_dict()
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
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 ):
        super().__init__(name=name,
                         type='sheet',
                       material=material,
                       fixed_size=fixed_size,
                       min_size=min_size,
                       max_size=max_size)  
        self.face_orientation = face_orientation
        o = self.face_orientation
        if self.min_size[o] is not None:
            get_logger().warning(f'min_size specified along orientation {o} is overwritten by thicnkess.')
            self.min_size.dim[o] = thickness
        if self.max_size[o] is not None:
            get_logger().warning(f'max_size specified along orientation {o} is overwritten by thicnkess.')
            self.max_size.dim[o] = thickness
        self.volume.size.dim[o] = thickness
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
        return f'{self.material.name}_{self.thickness}mm'

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
            face_orientation=d['face_orientation'],
            min_size=Size.from_dict(d['min_size']),
            max_size=Size.from_dict(d['max_size']))
        obj.volume = Volume.from_dict(d['volume'])
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
                 fixed_size:Size=Size(None,None,None),
                 min_size:Size=Size(0,0,0),
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY)):
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
                       face_orientation=face_orientation,
                       fixed_size=fixed_size,
                       max_size=max_size,
                       min_size=min_size)
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
        return Board(
            name=d['name'],
            material=Material.from_dict(d['material']),
            thickness=d['thickness'],
            face_orientation=d['face_orientation'],
            min_size=Size.from_dict(d['min_size']),
            max_size=Size.from_dict(d['max_size']),
            coating=CoatingSpec.from_dict(d['coating']))

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
        self.orientation = orientation
        self.length = length
        self.thickness = thickness
        self.width = width
        if self.orientation == Z_COORD: # weird for a guide but ok..., assume it is attached to a frontal plane
            fixed_size = Size(self.thickness,self.width,self.length)
        elif self.orientation == X_COORD: # a little less weird, assume attached to a vertical plane
            fixed_size = Size(self.length,self.thickness,self.width)
        elif self.orientation == Y_COORD: # most common, assume it is attached to a vertical plane
            fixed_size = Size(self.thickness,self.length,self.width)
        else:
            raise ValueError(f'Invalid guide orientation {self.orientation}.')

        super().__init__(name=name,
                         type='guide',
                         material=GUIDE_MATERIAL,
                         fixed_size=fixed_size)


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
            size = Size(self.head_width,self.head_width,self.length)
        elif self.direction == LEFT_TO_RIGHT or self.direction == RIGHT_TO_LEFT:        
            size = Size(self.length, self.head_width,self.head_width)
        elif self.direction == FRONT_TO_BACK or self.direction == BACK_TO_FRONT:        
            size = Size(self.head_width,self.length,self.head_width)
        else:
             raise ValueError(f'Invalid direction {self.direction}.')
        super().__init__(name=name, type=type, material=material,fixed_size=size)
    
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
