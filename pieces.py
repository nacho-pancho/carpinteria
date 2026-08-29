
from util import *
from core import *
from pieces import *
from materials import *

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
                 fixed_length:float=None,
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

        if fixed_length is not None:
            min_size.dim[orientation] = fixed_length
            max_size.dim[orientation] = fixed_length

        super().__init__(name=name,
                       material=material,
                       min_size=min_size,
                       max_size=max_size)  
        self.orientation = orientation
        self.screws = list()

    def type(self):
        return 'beam'


    def id(self):
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
        return f'{self.material.name}_{self.thickness}mm_x_{self.thickness}mm'

    def add_screw(self,position:Vector):
        pass

    def part_list(self):
        ret = list()
        ret.append(self.id())
        for s in self.screws():
            ret.append(s.id())

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
                       material=material,
                       fixed_size=fixed_size,
                       min_size=min_size,
                       max_size=max_size)  
        print(self)   
        self.face_orientation = face_orientation
        o = self.face_orientation
        if self.min_size[o] is not None:
            get_logger().warning(f'min_size specified along orientation {o} is overwritten by thicnkess.')
            self.min_size.dim[o] = thickness
        if self.max_size[o] is not None:
            get_logger().warning(f'max_size specified along orientation {o} is overwritten by thicnkess.')
            self.max_size.dim[o] = thickness
        self.volume.size.dim[o] = thickness
        self.screws = list()

    def type(self):
        return 'sheet'
    
    def id(self):
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

#--------------------------------------------------------------------

class CoatingSpec(SizeModifier):
    """
    Coating on a board can be applied to any side
    it is identical to a SizeModifier in every aspect, so we reuse the class.
    a value of 0 means no coating on a side.
    a nonzero value specifies its thickness.
    """
    def __init__(self,_size=0):
        super().__init__('Margin',_size)

    def __str__(self)->str:
            return super().__str__()

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
        self.coating = coating

    def id(self)->str:
        return super().id(self)

    def part_list(self):
        ret = list()
        ret.append(self.id())
        for s in self.screws():
            ret.append(s.id())

    def type(self):
        return 'board'

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

        super().__init__(name=name,material=materials.GUIDE_MATERIAL,fixed_size=fixed_size)


    def id(self)->str:
        return f'{self.type()}_{self.length}mm'

    def type(self):
        return 'drawer_guide'

    def part_list(self):
        ret = list()
        ret.append(self.id())


#--------------------------------------------------------------------

class NailLike(Piece):
    """
    A little thing with a beam and a head, like a screw or a nail
    """

    def __init__(self,name, material, caliber, length, direction):
        self.caliber = caliber
        self.length = length
        self.direction = direction
        self.radius = caliber / 2

        if self.direction == BOTTOM_TO_TOP or self.direction == TOP_TO_BOTTOM:        
            size = Size(2*self.head_radius,2*self.head_radius,self.length)
        elif self.direction == LEFT_TO_RIGHT or self.direction == RIGHT_TO_LEFT:        
            size = Size(self.length, 2*self.head_radius,2*self.head_radius)
        elif self.direction == FRONT_TO_BACK or self.direction == BACK_TO_FRONT:        
            size = Size(2*self.head_radius,self.length,2*self.head_radius)
        else:
            raise ValueError(f'Invalid direction {self.direction}.')
        super().__init__(name=name,material=material,fixed_size=size)
    
    def part_list(self):
        ret = list()
        ret.append(self.id())

#--------------------------------------------------------------------

class Screw(NailLike):
    """
    a screw. 
    """

    def __init__(self,name, material, caliber, length, direction):
        super().__init__(name,material,caliber,length,direction)

    def type(self)->str:
        return 'screw'

    def id(self)->str:
        return f'{self.type()}_{self.caliber}mm_x_{self.length}mm'

#--------------------------------------------------------------------

class Nail(NailLike):
    """
    Dowel or Dowel pin in English
    Tarugo in spanish (only way I can remember this)
    Small peg of wood used to join two boards or something like that
    """

    def __init__(self,name, caliber, length, direction):
        super().__init__(name,NAIL_MATERIAL,caliber,length,direction)

    def type(self)->str:
        return 'nail'

    def id(self)->str:
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
                         material=DOWEL_MATERIAL,
                         caliber=6,
                         length=length,
                         direction=direction)

    def type(self):
        return 'dowel'

    def id(self)->str:
        return f'{self.type()}_{self.length}mm'


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
        super().__init__(name,CORNER_MATERIAL,fixed_size=size)

    def type(self):
        return 'corner_brace'

    def id(self):
        return self.type()

#--------------------------------------------------------------------
