"""
functions to create complex pieces
"""
from pieces import *
from layout import *
from geometry import *
from core import *
from util import *

def mdf(name, thickness, face_orientation, color_name='white'):
    """
    Creates a coated MDF piece with coating added to both faces automatically
    """
    coating = CoatingSpec()
    print(coating.values,face_orientation)
    coating.values[face_orientation][0] = coating.values[face_orientation][1] = 1
    material = create_mdf_material(color_name)
    return Board(name=name,material=material,thickness=thickness,coating=coating,face_orientation=face_orientation)


def build_drawer(size:Size):
    # drawer is built as 4 nested stacks
    # the first one goes front to back and includes the drawer front in slot 1, and the middle stack as the slot 2
    # the second stack contains 3 slots: the sides and an container in the middle for the base and the back
    # the third is an vertical (Z) stack with the drawer volume and back on top, and the base in the bottom (slot 2)
    # the last stack goest from to back and contains an empty volume (slot 1) and the back (slot 2)
    #
    # stack 1: front and body
    stack_1 = CompositePiece("stack 1 of 4", fixed_size =size, layout=StackLayout(2,Y_COORD))
    front = mdf("front",15,Y_COORD,'white')
    cons = LayoutConstraints()
    stack_1.add_piece(front,cons,0)
    # stack 2: sides and inner body
    stack_2 = CompositePiece("stack 2 of 4", layout=StackLayout(3,X_COORD))
    left_side = mdf("left_side",15,X_COORD,'red')
    cons = LayoutConstraints()
    stack_2.add_piece(left_side,cons,0)

    stack_3 = CompositePiece("stack 3 of 4", layout=StackLayout(2,Z_COORD))
    cons = LayoutConstraints()
    # stack 3: inner volume and base
    base = mdf("base",15,Z_COORD,'yellow')
    cons = LayoutConstraints()
    stack_3.add_piece(base,cons,0)
    # stack 4: inner volume and back
    stack_4 = CompositePiece("stack 4 of 4", layout=StackLayout(2,Y_COORD))
    cons = LayoutConstraints()
    stack_4.add_piece(Void("drawer_contents"),cons,0)
    back = mdf("back",15,Y_COORD,'blue')
    cons = LayoutConstraints()
    stack_4.add_piece(back,cons,1)
    # back to stack 3
    stack_3.add_piece(stack_4,cons,1)

    # back to stack 2
    cons = LayoutConstraints()
    stack_2.add_piece(stack_3,cons,1)

    right_side = mdf("right_side",15,X_COORD,'green')
    cons = LayoutConstraints()
    stack_2.add_piece(right_side,cons,2)

    # back to stack 1
    cons = LayoutConstraints()
    stack_1.add_piece(stack_2,cons,1)
    return stack_1




def basic_desk():
    """
    a desk with the very basic structure
    """
    pass

def desk_with_drawers():
    """
    a desk with a side with drawers
    """
    pass

def night_table():
    """
    a simple night table with 3 drawers 
    """
    pass

def comoda():
    """
    sorry name in spanish is clearer
    """

def aparador():
    """
    sorry name in spanish is clearer here too
    """

def closet():
    """
    a simple closet 
    """

def bed():
    """
    parametric bed
    """