#!/usr/bin/env python3

from util import *
from core import *
from materials import *
from pieces import *
from materials import *
from display import *
from json_backend import *

def test_pyvista():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    sphere = pv.Sphere()
    pl.add_mesh(sphere,color='red',opacity=0.5,show_edges=True)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()


def test_box_sides():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    box = pv.Box((0,1,0,2,0,3))
    print(box.faces)
    color_idx = (1,0,0,0,0,0)
    pl.add_mesh(box,color='blue',opacity=1,show_edges=True,scalars=color_idx,cmap='jet')   
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()

def test_void():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    size = Size(10,20,30)
    piece =  Void(name='a void',fixed_size=size)
    print(piece)

    # test I/O
    proj = Project(name='Test void',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_void.json',proj)
    proj2 = load_project('test_void.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_void_reloaded.json',proj2)

    # test display
    paint(pl,piece)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()

def test_composite():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    comp = CompositePiece('Compuesto de nada',fixed_size=Size(100,200,300))
    piece =  Void(Size(10,None,30))
    cons = LayoutConstraints()
    cons.margin = Margin((10,20,30,40,50,60)) # +30, +70, + 110
    cons.padding = Padding((1,2,3,4,5,6))     # -3, -7, - 11
    comp.add_piece(piece,cons)
    enable_tracing()
    comp.apply_layout()

    # test I/O
    proj = Project(name='Test composite',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_composite.json',proj)
    proj2 = load_project('test_composite.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_composite_reloaded.json',proj2)

    # test display
    paint(pl,comp)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()


def test_stack():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()

    # works
    comp = CompositePiece('Compuesto de nada',
                               fixed_size=Size(100,200,300),
                               layout=StackLayout(num_slots=3,axis=Z_COORD))

    piece = Void(fixed_size=Size(None,None,20)) # fix height    
    cons = LayoutConstraints()
    cons.margin = Margin((5,5,5,5,10,20)) 
    cons.padding = Padding((0,0,0,0,0,0))
    comp.add_part(piece,cons,0)

    piece = Void(fixed_size=Size(None,None,40)) # fix height    
    cons = LayoutConstraints()
    cons.margin = Margin((5,5,5,5,10,10)) 
    cons.padding = Padding((0,0,0,0,0,0))
    comp.add_part(piece,cons,1)

    piece = Void(fixed_size=Size(None,None,60)) # fix height    
    cons = LayoutConstraints()
    cons.margin = Margin((5,5,5,5,10,10)) 
    cons.padding = Padding((20,0,0,0,0,0))
    comp.add_part(piece,cons,2)

    comp.apply_layout()

    # test I/O
    proj = Project(name='Test stack',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_stack.json',proj)
    proj2 = load_project('test_stack.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_stack_reloaded.json',proj2)

    # test display
    enable_tracing()
    paint(pl,comp)
    print(comp)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()

def test_beam():
    # works
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  Beam('a beam',
                        material=FINGER_MATERIAL,
                        thickness1=40,
                        thickness2=40,
                        orientation=X_COORD,
                        length=1000)

    # test I/O
    proj = Project(name='Test beam',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_beam.json',proj)
    proj2 = load_project('test_beam.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_beam_reloaded.json',proj2)

    paint(pl,piece)  
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()


def test_sheet():
    # works
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  Sheet('sheet',
                        material=FINGER_MATERIAL,
                        thickness=20,
                        face_orientation=Z_COORD,
                        fixed_size=Size(1000,600,None))

    # test I/O
    proj = Project(name='Test sheet',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_sheet.json',proj)
    proj2 = load_project('test_sheet.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_sheet_reloaded.json',proj2)

    paint(pl,piece)  
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()


def test_board():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  Board('board',
                        material=MDF_MATERIAL,
                        thickness=18,
                        face_orientation=Z_COORD,
                        coating=CoatingSpec((1,1,0,0,1,1)),
                        fixed_size=Size(1000,600,None))
    # test I/O
    proj = Project(name='Test board',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_board.json',proj)
    proj2 = load_project('test_board.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_board_reloaded.json',proj2)

    # test display
    paint(pl,piece)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()


def test_guide():
    # works
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  DrawerGuide('guide',
                        orientation=Y_COORD,
                        length=400)


    # test I/O
    proj = Project(name='Test guide',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_guide.json',proj)
    proj2 = load_project('test_guide.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_guide_reloaded.json',proj2)

    # test display
    paint(pl,piece)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()

def test_screw():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  Screw(name='screw',
                   material=FLAT_SCREW_MATERIAL,
                   caliber=3,
                   length=15,
                   direction=TOP_TO_BOTTOM)

    # test I/O
    proj = Project(name='Test screw',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_screw.json',proj)
    proj2 = load_project('test_screw.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_screw_reloaded.json',proj2)

    # test display
    paint(pl,piece)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()


def test_nail():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  Nail(name='nail',
                   caliber=3,
                   length=40,
                   direction=TOP_TO_BOTTOM)

    # test I/O
    proj = Project(name='Test nail',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_nail.json',proj)
    proj2 = load_project('test_nail.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_nail_reloaded.json',proj2)

    # test display
    paint(pl,piece)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()


def test_dowel():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  Dowel(name=' a dowel',length=40,direction=TOP_TO_BOTTOM)

    # test I/O
    proj = Project(name='Test dowel',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_dowel.json',proj)
    proj2 = load_project('test_dowel.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_dowel_reloaded.json',proj2)

    # test display
    paint(pl,piece)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()

def test_corner():
    get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()
    piece =  CornerBrace(name='a corner',orientation=X_COORD)

    # test I/O
    proj = Project(name='Test corner',version='1.0',date='1/1/1',author='Ignacio Ramirez',description='bah')
    proj.add_piece(piece)
    print('PROJECT CREATED')
    print(proj)
    print(proj.to_dict())
    save_project('test_corner.json',proj)
    proj2 = load_project('test_corner.json')
    print('LOADED PROJECT')
    print(proj2)
    print(proj2.to_dict())
    save_project('test_corner_reloaded.json',proj2)

    # test display
    paint(pl,piece)
    pl.add_floor('-z',color='gray',lighting=True,pad=0.5) 
    pl.view_vector((0,-5,0))
    pl.show_axes()
    pl.show_grid()
    pl.show()

if __name__ == '__main__':
    test_void()
    test_nail() # did not show 
    test_dowel() # did not show
    test_screw() # shows but wrong
    test_beam()
    test_sheet()
    test_board()
    test_composite()
    test_stack()






