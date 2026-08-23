#!/usr/bin/env python3

import pyvista as pv
import pyvista.core.utilities as pvutil
import numpy as np

import carp

trace = False
def enable_tracing():
    global trace
    trace = True

def disable_tracing():
    global trace
    trace = False


def paint_board(plotter:pv.Plotter, obj:carp.Board):
    return plotter

def paint_sheet(plotter:pv.Plotter, obj:carp.Sheet):
    return plotter


def paint_void(plotter:pv.Plotter, obj:carp.Void):

    x_0 = obj.volume.offset[0]
    x_1 = x_0 + obj.volume.size[0]
    y_0 = obj.volume.offset[1]
    y_1 = y_0 + obj.volume.size[1]
    z_0 = obj.volume.offset[2]
    z_1 = z_0 + obj.volume.size[2]
    box = pv.Box((x_0,x_1,y_0,y_1,z_0,z_1))
    plotter.add_mesh(box,show_edges=True,style='wireframe')
    return plotter

def paint_volume(plotter:pv.Plotter, volume:carp.Volume, color='gray'):
    x_0 = volume.offset[0]
    x_1 = x_0 + volume.size[0]
    y_0 = volume.offset[1]
    y_1 = y_0 + volume.size[1]
    z_0 = volume.offset[2]
    z_1 = z_0 + volume.size[2]
    box = pv.Box((x_0,x_1,y_0,y_1,z_0,z_1))
    plotter.add_mesh(box,show_edges=True,style='wireframe',color=color)
    return plotter

def paint_screw(plotter:pv.Plotter, obj:carp.Screw):
    return plotter

def paint_drawer_guide(plotter:pv.Plotter, obj:carp.DrawerGuide):
    return plotter

def paint_composite(plotter:pv.Plotter,obj:carp.CompositePiece):
    for part in obj.parts:
        if trace:
            plotter = paint_volume(plotter,part.base_volume,'green')
            plotter = paint_volume(plotter,part.padded_volume,'blue')
            print(f'Available volume {part.available_volume}')
            plotter = paint_volume(plotter,part.available_volume,'magenta')
            plotter = paint_volume(plotter,part.piece_volume, 'red')
        if part is not None:
            plotter = paint(plotter,part.piece)
    return plotter

def paint(plotter:pv.Plotter,obj):
    if type(obj) == carp.Board:
        return paint_board(plotter,obj)
    elif type(obj) == carp.Sheet:
        return paint_sheet(plotter,obj)
    elif type(obj) == carp.Void:
        return paint_void(plotter,obj)
    elif type(obj) == carp.Screw:
        return paint_screw(plotter,obj)
    elif type(obj) == carp.DrawerGuide:
        return paint_drawer_guide(plotter,obj)
    elif type(obj) == carp.CompositePiece:
        return paint_composite(plotter,obj)

import logging

if __name__ == '__main__':
    carp.get_logger().setLevel(logging.DEBUG)
    pl = pv.Plotter()

    # works
    #sphere = pv.Sphere()
    #pl.add_mesh(sphere,color='red',opacity=0.5,show_edges=True)

    # works
    #box = pv.Box((0,1,0,2,0,3))
    #print(box.faces)
    #color_idx = (1,0,0,0,0,0)
    #pl.add_mesh(box,color='blue',opacity=1,show_edges=True,scalars=color_idx,cmap='jet')   

    #size = carp.Size(10,20,30)
    #piece =  carp.Void(size)
    #print(piece)
    #paint(pl,piece)
    #pl.add_floor('-z',color='gray',lighting=True,pad=10) 
    #pl.view_vector((0,-5,0))
    #pl.show()
    #exit(1)

    # works
    comp = carp.CompositePiece('Compuesto de nada',fixed_size=carp.Size(100,200,300))
    piece =  carp.Void(carp.Size(10,None,30))
    print('PIECEE')
    print(piece)
    cons = carp.LayoutConstraints()
    print(cons)
    cons.margin = carp.Margin((10,20,30,40,50,60)) # +30, +70, + 110
    cons.padding = carp.Padding((1,2,3,4,5,6))     # -3, -7, - 11
    comp.add_piece(piece,cons)
    enable_tracing()
    comp.apply_layout()
    print(comp)
    paint(pl,comp)
    pl.add_floor('-z',color='gray',lighting=True,pad=10) 
    pl.view_vector((0,-5,0))
    pl.show()
    exit(1)


    # test
    cons = carp.LayoutConstraints()
    cons.margin = carp.Margin((10,20,30,40,50,60)) # +30, +70, + 110
    cons.padding = carp.Padding((1,2,3,4,5,6))     # -3, -7, - 11
    cons.alignment[0] = carp.LEFT
    cons.alignment[1] = carp.CENTER
    cons.alignment[2] = carp.RIGHT
    # total +27, +63, +99
    size = carp.Size(10,None,30) # leave depth unspecified
    piece = carp.Void(size)
    comp.add_piece(piece,cons)
    comp.apply_layout()
    enable_tracing()
    print(trace)
    paint(pl,comp)
    print(comp)
    pl.add_floor('-z',color='gray',lighting=True,pad=10) 
    pl.view_vector((0,-5,0))
    pl.show()
    exit(1)

    layout = carp.StackLayout(2,carp.X_COORD)

    piece =  carp.Void(size)
    piece.min_size.dim[2] = 10
    piece.max_size.dim[1] = 17
    piece.max_size.dim[0] = 19
    piece.max_size.dim[2] = 23   
    cons = carp.LayoutConstraints()
    cons.margin = carp.Margin((0,0,0,0,0,0))
    cons.padding = carp.Padding((0,0,0,0,0,0))
    cons.alignment[0] = carp.CENTER
    cons.alignment[1] = carp.CENTER
    cons.alignment[2] = carp.CENTER

    comp.add_piece(piece,cons)
    comp.apply_layout()
    enable_tracing()
    print(trace)
    paint(pl,comp)
    print(comp)
    pl.add_floor('-z',color='gray',lighting=True,pad=10) 
    pl.view_vector((0,-5,0))
    pl.show()



