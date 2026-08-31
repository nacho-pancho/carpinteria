#!/usr/bin/env python3

import pyvista as pv
import pyvista.core.utilities as pvutil
import numpy as np

from util import *
from core import *
from materials import *
from pieces import *
from materials import *
import copy

trace = False
def enable_tracing():
    global trace
    trace = True

def disable_tracing():
    global trace
    trace = False

def volume_to_box(v:Volume):
    return (
        v.offset[0],
        v.offset[0]+v.size[0],
        v.offset[1],
        v.offset[1]+v.size[1],
        v.offset[2],
        v.offset[2]+v.size[2],
        )


def paint_volume(plotter:pv.Plotter, volume:Volume, color='gray'):
    box = pv.Box(volume_to_box(volume))
    plotter.add_mesh(box,show_edges=True,style='wireframe',color=color)
    return plotter


def paint_void(plotter:pv.Plotter, obj:Void):
    box = pv.Box(volume_to_box(obj.volume))
    plotter.add_mesh(box,show_edges=True,style='wireframe')
    return plotter

def paint_obj(plotter:pv.Plotter,obj:pv.PolyData,tex:Texture):
    if tex.texture_map is not None:
        tex_map = pv.read_texture(tex.texture_map)
    else:
        tex_map = None
    plotter.add_mesh(obj,show_edges=False,
                     color=tex.color,
                     ambient=tex.ambient,
                     diffuse=tex.diffuse,
                     metallic=tex.metallic,
                     specular=tex.specular,
                     specular_power=tex.specular_power,
                     roughness=tex.roughness,
                     texture=tex_map)
    return plotter

def paint_block(plotter:pv.Plotter, obj:Sheet):
    size = obj.volume.size
    orig = obj.volume.offset
    box = pv.Box(volume_to_box(obj.volume))
    material = obj.material
    texture = material.exterior
    if texture.texture_map is not None:
        box.texture_map_to_plane(origin=orig.coords,point_u=(size[0],0,0),point_v=(0,size[1],0),inplace=True)
    plotter = paint_obj(plotter,box,texture)
    return plotter

def paint_sheet(plotter:pv.Plotter, obj:Sheet):
    size = obj.volume.size
    orig = obj.volume.offset
    box = pv.Box(volume_to_box(obj.volume))
    material = obj.material
    texture = material.exterior
    if texture.texture_map is not None:
        if obj.face_orientation == Z_COORD:
            box.texture_map_to_plane(origin=orig.coords,point_u=(size[0],0,0),point_v=(0,size[1],0),inplace=True)
        elif obj.face_orientation == Y_COORD:
            box.texture_map_to_plane(origin=orig.coords,point_u=(size[0],0,0),point_v=(0,0,size[2]),inplace=True)
        elif obj.face_orientation == X_COORD:
            box.texture_map_to_plane(origin=orig.coords,point_u=(0,size[1],0),point_v=(0,0,size[2]),inplace=True)
    plotter = paint_obj(plotter,box,texture)
    return plotter


def paint_beam(plotter:pv.Plotter, obj:Beam):
    size = obj.volume.size
    orig = obj.volume.offset
    box = pv.Box(volume_to_box(obj.volume))
    material = obj.material
    texture = material.exterior
    if texture.texture_map is not None:
        if obj.orientation == Z_COORD:
            box.texture_map_to_plane(origin=orig.coords,point_u=(size[0],0,0),point_v=(0,size[1],0),inplace=True)
        elif obj.orientation == Y_COORD:
            box.texture_map_to_plane(origin=orig.coords,point_u=(size[0],0,0),point_v=(0,0,size[2]),inplace=True)
        elif obj.orientation == X_COORD:
            box.texture_map_to_plane(origin=orig.coords,point_u=(0,size[1],0),point_v=(0,0,size[2]),inplace=True)
    plotter = paint_obj(plotter,box,texture)
    return plotter


def paint_drawer_guide(plotter:pv.Plotter, obj:DrawerGuide):
    box = pv.Box(volume_to_box(obj.volume))
    return paint_obj(plotter,box,obj.material.exterior)


def paint_board(plotter:pv.Plotter, obj:Board):
    volume = obj.volume
    size = volume.size
    orig = volume.offset
    coating = obj.coating
    coating_size =coating.size()
    coating_off = coating.offset()
    int_vol = shrink_volume(volume,coating)
    int_box = pv.Box(volume_to_box(int_vol))
    int_tex = obj.material.interior
    ext_tex = obj.material.exterior

    if ext_tex.texture_map is not None:
        ext_tex_map = pv.read_texture(ext_tex.texture_map)
    else:
        ext_tex_map = None
    if int_tex.texture_map is not None:
        int_tex_map = pv.read_texture(int_tex.texture_map)
    else:
        int_tex_map = None
    # 
    # interior of board made of MDF
    #
    plotter = paint_obj(plotter,int_box,int_tex)
    #
    # paint coating, one face at a time
    #
    for i in range(3):
        if coating[i][0] > 0:
            coat_thk = coating[i][0]
            coat_vol = copy.deepcopy(volume)
            coat_vol.size.dim[i] = coat_thk
            coat_box = pv.Box(volume_to_box(coat_vol))
            plotter = paint_obj(plotter,coat_box,ext_tex)

        if coating[i][1] > 0:
            coat_thk = coating[i][1]
            coat_vol = copy.deepcopy(volume)
            coat_vol.size.dim[i] = coat_thk
            coat_vol.offset.coords[i] = volume.size.dim[i] - coat_thk
            coat_box = pv.Box(volume_to_box(coat_vol))
            plotter = paint_obj(plotter,coat_box,ext_tex)
    return plotter


def paint_nail_like(plotter:pv.Plotter, obj:NailLike):
    #
    volume = obj.volume # this is actually the bounding box
    offset = volume.offset
    size   = volume.size
    tex = obj.material.exterior
    #
    # we don't support arbitrary directions
    # so we treat each direction separtely
    # not very elegant but very simple to implement without errors
    #
    # base_pos lies inside the screw at the center of the junction of the beam with the head
    beam_center = [
        offset.coords[0] + size.dim[0]/2,
        offset.coords[1] + size.dim[1]/2,
        offset.coords[2] + size.dim[2]/2]
    beam_height = obj.length
    head_height = obj.head_height
    beam_radius = obj.caliber / 2 
    head_width = obj.head_width
    head_shift  = ( head_height + beam_height ) / 2
    head_center = [
        offset.coords[0] + size.dim[0]/2,
        offset.coords[1] + size.dim[1]/2,
        offset.coords[2] + size.dim[2]/2]
    if obj.direction == BACK_TO_FRONT:
        head_center[1] += head_shift
        cyl_dir = (0,1,0)
    elif obj.direction == FRONT_TO_BACK:
        head_center[1] -= head_shift
        cyl_dir = (0,1,0)
    elif obj.direction == RIGHT_TO_LEFT:
        head_center[0] += head_shift
        cyl_dir = (1,0,0)
    elif obj.direction == LEFT_TO_RIGHT:
        head_center[0] -= head_shift
        cyl_dir = (1,0,0)
    elif obj.direction == TOP_TO_BOTTOM:
        head_center[2] += head_shift
        cyl_dir = (0,0,1)
    elif obj.direction == BOTTOM_TO_TOP:
        head_center[2] -= head_shift
        cyl_dir = (0,0,1)
    else:
        raise ValueError(f'Invalid direction')
    if head_height > 0:
        pd = pv.Cylinder(center=head_center,direction=cyl_dir,radius=head_width/2,height=head_height)
        plotter = paint_obj(plotter,pd,tex)
    pd = pv.Cylinder(center=beam_center,direction=cyl_dir,radius=beam_radius,height=beam_height)
    plotter = paint_obj(plotter,pd,tex)

    return plotter


def paint_composite(plotter:pv.Plotter,obj:CompositePiece):
    for part in obj.piece_specs:
        if trace:
            plotter = paint_volume(plotter,part.slot_volume,'green')
            plotter = paint_volume(plotter,part.padded_volume,'blue')
            plotter = paint_volume(plotter,part.available_volume,'magenta')
            plotter = paint_volume(plotter,part.piece_volume, 'red')
        if part is not None:
            plotter = paint(plotter,part.piece)
    return plotter

def paint(plotter:pv.Plotter,obj):
    if type(obj) == Board:
        return paint_board(plotter,obj)
    elif type(obj) == Sheet:
        return paint_sheet(plotter,obj)
    elif type(obj) == Void:
        return paint_void(plotter,obj)
    elif type(obj) == DrawerGuide:
        return paint_drawer_guide(plotter,obj)
    elif type(obj) == CompositePiece:
        return paint_composite(plotter,obj)
    elif isinstance(obj,NailLike):
        return paint_nail_like(plotter,obj)
    elif isinstance(obj,Beam):
        return paint_beam(plotter,obj)
    elif isinstance(obj,Block):
        return paint_block(plotter,obj)
    else:
        print(f"Don't know how to paint {obj}")


