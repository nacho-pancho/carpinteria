import copy
import math
from dataclasses import dataclass
from jsonable import JSONable
#
# coordinates/orientatios
#
X_COORD = 0
Y_COORD = 1
Z_COORD = 2

#
# anchors
#
BACK   = 'back'
FRONT  = 'front'
LEFT   = 'left'
RIGHT  = 'right'
TOP    = 'top'
BOTTOM = 'bottom'
CENTER = 'center'

#
# directions
#
FRONT_TO_BACK = '+y'
BACK_TO_FRONT = '-y'
BOTTOM_TO_TOP = '+z'
TOP_TO_BOTTOM = '-z'
LEFT_TO_RIGHT = '+x'
RIGHT_TO_LEFT = '-x'


INFINITY = 1000000000 # 1000km is quite large for a furniture
#
# ==========================================================
# Basic types
# ==========================================================
#

#--------------------------------------------------------------------

class Vector(JSONable):

    def __init__(self,x=0,y=0,z=0):
        if type(x) == list or type(x) == tuple:
                raise ValueError('Vector takes 3 scalars.')
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

    def to_dict(self):
        return self.coords # already serializable

    def from_dict(d): # this would be a list or tuple, not a dict
        return Vector(*d)
    

def translate_vector(a:Vector,b:Vector|Size):
    ret = Vector()
    if type(b) == Vector:
        ret.coords[0] = a.coords[0] + b.coords[0]
        ret.coords[1] = a.coords[1] + b.coords[1]
        ret.coords[2] = a.coords[2] + b.coords[2]
    elif type(b) == Size:
        ret.coords[0] = a.coords[0] + b.dim[0]
        ret.coords[1] = a.coords[1] + b.dim[1]
        ret.coords[2] = a.coords[2] + b.dim[2]
    return ret

#--------------------------------------------------------------------

# conceptully different but same thing inside
type Point = Vector

#--------------------------------------------------------------------

class Size(JSONable):

    def __init__(self,sx:float=0, sy:float=0, sz:float=0):
        if type(sx) == list or type(sx) == tuple:
            raise ValueError("Size initializer takes 3 scalars")
        self.dim = [sx,sy,sz]


    def width(self): 
        return self.dim[X_COORD]


    def height(self):
        return self.dim[Z_COORD]


    def depth(self):
        return self.dim[Y_COORD]

    
    def grow(self,amount:Size | SizeModifier):
        if isinstance(amount,SizeModifier):
            size = amount.size()
        else:
            size = amount
        if self.dim[X_COORD] is not None:
            self.dim[X_COORD] += size.dim[X_COORD]
        if self.dim[Y_COORD] is not None:
            self.dim[Y_COORD] += size.dim[Y_COORD]
        if self.dim[Z_COORD] is not None:
            self.dim[Z_COORD] += size.dim[Z_COORD]

    def shrink(self,amount:Size | SizeModifier):
        if isinstance(amount,SizeModifier):
            size = amount.size()
        else:
            size = amount
            if self.dim[X_COORD] is not None:
                self.dim[X_COORD] -= size.dim[X_COORD]
            if self.dim[Y_COORD] is not None:
                self.dim[Y_COORD] -= size.dim[Y_COORD]
            if self.dim[Z_COORD] is not None:
                self.dim[Z_COORD] -= size.dim[Z_COORD]

    def __getitem__(self,i):
        return self.dim[i]

    def defined(self):
        return self.dim[0] is not None and self.dim[1] is not None and self.dim[2] is not None
    
    def __str__(self):
        return self.dim.__str__()

    def to_dict(self):
        return self.dim # already serializable

    def from_dict(d): # a list or tuple
         return Size(*d)
    
    
def grow_size(a:Size,b:Size | SizeModifier):
    ret = copy.copy(a)
    ret.grow(b)
    return ret

def shrink_size(a:Size,b:Size | SizeModifier):
    ret = copy.copy(a)
    ret.shrink(b)
    return ret

#--------------------------------------------------------------------

@dataclass
class Volume(JSONable):
    """
    A rectangular region in space
    """
    size:Size
    offset:Vector # lower left front corner

    def __init__(self,size:Size=Size(),off:Vector=Vector()):
        self.size = size
        self.offset = off


    def grow(self,p:SizeModifier):
        """
        padding enlarges the volume and shifts the offset outwards
        """
        for i in range(3):
            self.size.dim[i] += p[i][1] + p[i][0]
            self.offset.coords[i] -= p[i][0]

    def shrink(self,m:SizeModifier):
        """
        margin reduces the volume and shifts the offset to the interior
        """
        for i in range(3):
            self.size.dim[i] -= m[i][1] + m[i][0]
            self.offset.coords[i] += m[i][0]


    def __str__(self):
        return f'Volume of size {self.size} at offset {self.offset}'

    def to_dict(self):
        return {"size":self.size.to_dict(), "offset": self.offset.to_dict() }

    def from_dict(d:dict):
        return Volume(Size.from_dict(d['size']),Vector.from_dict(d['offset']))


def grow_volume(v:Volume,p:Padding):
    ret = copy.deepcopy(v)
    ret.grow(p)
    return ret


def shrink_volume(v:Volume,m:Margin):
    ret = copy.deepcopy(v)
    ret.shrink(m)
    return ret

#--------------------------------------------------------------------

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
        print(_size)
        if type(_size) == tuple or type(_size) == list:
            if len(_size) == 6:
                for i in range(3):
                    self.values[i] = _size[2*i:2*(i+1)]
            elif len(_size) == 3:
                for i in range(3):
                    _size_i = _size[i]
                    print(_size_i)
                    if type(_size_i) == tuple or type(_size_i) == list:
                        if len(_size_i) == 2:
                            self.values[i][0] = _size_i[0]
                            self.values[i][1] = _size_i[1]
                        else:
                            raise ValueError(f'{_type} argument must be either a scalar, a tuple of 3, a tuple of 6, or a tuple of 3 tuples of 2')  
                    else:
                        self.values[i][0] = self.values[i][1] = _size_i # same value left and right                          
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

    def size(self):
        sx = self.values[X_COORD][0] + self.values[X_COORD][1]
        sy = self.values[Y_COORD][0] + self.values[Y_COORD][1]
        sz = self.values[Z_COORD][0] + self.values[Z_COORD][1]
        return Size(sx,sy,sz)

    def offset(self):
        ox = self.values[X_COORD][0]
        oy = self.values[Y_COORD][0]
        oz = self.values[Z_COORD][0]
        return Vector(ox,oy,oz)

    def to_dict(self):
        return self.values


#--------------------------------------------------------------------

class Padding(SizeModifier):
    def __init__(self,_size=0):
        super().__init__('Padding',_size)


    def __str__(self):
        return super().__str__()

    
    def from_dict(d): # type is not really important
        return SizeModifier('padding',d)

#--------------------------------------------------------------------

class Margin(SizeModifier):
    def __init__(self,_size=0):
        super().__init__('Margin',_size)

    def __str__(self):
            return super().__str__()

    def from_dict(d): # type is not really important
        return SizeModifier('margin',d)

#--------------------------------------------------------------------


type Weight = Vector

