#!/usr/bin/env python3

import pyvista as pv
import pyvista.core.utilities as pvutil
import numpy as np

import carp

def paint_board(plotter:pv.Plotter, obj:carp.Board):
    return plotter

def paint_sheet(plotter:pv.Plotter, obj:carp.Sheet):
    return plotter

def paint_void(plotter:pv.Plotter, obj:carp.Void):
    x_0 = obj.offset[0]
    x_1 = x_0 + obj.size[0]
    y_0 = obj.offset[1]
    y_1 = y_0 + obj.size[1]
    z_0 = obj.offset[2]
    z_1 = z_0 + obj.size[2]
    box = pv.Box(x_0,x_1,y_0,y_1,z_0,z_1)
    plotter.add_mesh(box,show_edges=True,style='wireframe')
    return plotter


def paint_screw(plotter:pv.Plotter, obj:carp.Screw):
    return plotter

def paint_drawer_guide(plotter:pv.Plotter, obj:carp.DrawerGuide):
    return plotter

def paint_composite(plotter:pv.Plotter,obj:carp.CompositePiece):
    for v in obj.volumes:
        p = v.piece
        if p is not None:
            plotter = paint(plotter,p)
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


if __name__ == '__main__':
    pl = pv.Plotter()
    #sphere = pv.Sphere()
    #pl.add_mesh(sphere,color='red',opacity=0.5,show_edges=True)
    size = (1,2,3)
    thing = carp.CompositePiece('vacio','nada',size=size)
    thing.add_piece(carp.Void())
    thing.apply_layout()
    paint(pl,thing)
 
    box = pv.Box((0,1,0,2,0,3))
    print(box.faces)
    color_idx = (1,0,0,0,0,0)
    pl.add_mesh(box,color='blue',opacity=1,show_edges=True,scalars=color_idx,cmap='jet')   
    pl.add_floor('-z',color='gray',lighting=True,pad=1) 
    pl.view_vector((0,-5,0))
    pl.show()
