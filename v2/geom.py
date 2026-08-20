import numpy as np
import math

def trans(v,dx,dy,dz):
    return (v[0] +dx, v[1]+dy, v[2] + dz)

def rot_x(v,grados):
    theta = grados*math.pi/180
    c,s = math.cos(theta), math.sin(theta)
    return (
        v[0],        
        c*v[1] - s*v[2],
        s*v[1] + c*v[2]
    )

def rot_y(v,grados):
    theta = grados*np.pi/180
    c,s = math.cos(theta), math.sin(theta)
    return (
        c*v[0] + s*v[2],
        v[1],
        -s*v[0] + c*v[2]
    )

def rot_z(v,grados):
    theta = grados*np.pi/180
    c,s = math.cos(theta), math.sin(theta)
    return (
        c*v[0] - s*v[1],
        s*v[0] + c*v[1],
        v[2]
    )

def rot(v,ax,ay,az):
    w = rot_x(v,ax)
    w = rot_y(w,ay)
    w = rot_z(w,az)
    return w
