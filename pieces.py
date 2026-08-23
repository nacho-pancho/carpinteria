
from util import *
from carp import *
from pieces import *

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

    def __str__(self):
            return super().__str__()

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
                 max_size:Size=Size(INFINITY,INFINITY,INFINITY),
                 top=False, 
                 bottom=False, 
                 left=False, 
                 right=False, 
                 back=False, 
                 front=False):
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
            material = materials.FLAT_SCREW_MATERIAL
            head_radius = caliber * 2
        elif self.type == Screw.WOOD:
            material = materials.WOOD_SCREW_MATERIAL
            head_radius = caliber
        material = f'screw_{_type}_{caliber}mmx{length}mm'
        min_size = (2*head_radius,2*head_radius,length)
        max_size = min_size
        size = min_size   
        super.__init__(name,material,size,min_size,max_size)

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
        material = materials.GUIDE_MATERIAL
        material = f'guide_{length}mm'
        min_size = (self.thickness,self.width,length)
        max_size = min_size
        size = min_size   
        super.__init__(name,material,size,min_size,max_size)
