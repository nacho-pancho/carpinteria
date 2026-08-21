#!/usr/bin/env python3

import pyvista as pv
import pyvista.core.utilities as pvutil
import numpy as np

import carp

def paint_board(obj:carp.Board):
    pass

def paint_sheet(obj:carp.Board):
    pass

def paint_void(obj:carp.Void):
    pass

def paint_screw(obj:carp.Screw):
    pass

def paint_guide(obj:carp.Guide):
    pass

def paint(obj):
    if type(obj) == carp.Board:
        paint_board(obj)
    elif type(obj) == carp.Sheet:
        paint_sheet(obj)
    elif type(obj) == carp.Void:
        paint_void(obj)


if __name__ == '__main__':
    pl = pv.Plotter()
    #sphere = pv.Sphere()
    #pl.add_mesh(sphere,color='red',opacity=0.5,show_edges=True)

    box = pv.Box((0,1,0,2,0,3))
    print(box.faces)
    color_idx = (1,0,0,0,0,0)
    pl.add_mesh(box,color='blue',opacity=1,show_edges=True,scalars=color_idx,cmap='jet')   
    pl.add_floor('-z',color='gray',lighting=True,pad=1) 
    pl.view_vector((0,-5,0))
    pl.show()
