#!/usr/bin/env python3
#
# -*- coding:utf-8 -*-
# 

import numpy as np

import cadquery as cq
import cadquery.vis as vis

import carpinteria
#
# agujero del living
# profundidad del agujero 60cm
# el agujero interno debería tener 40cm de profundidad
# 50cm es mucho
# capaz que 45cm es un buen tamaño
# largo 200cm pero es una locura hacer uno tan largo
# tiene puertas, no cajones
def aparador(nombre, 
        alto=1000,
        largo=800,
        prof=450, 
        z_base=500,
        grosor_mdf=18, 
        grosor_finger=20,
        h_bandeja=200,
        color=carpinteria.COLOR_BLANCO
    ):
    """
    " alto: altura total del mueble en mm
    " largo: largo total del mueble en mm
    " prof: profundidad total del mueble en mm
    " base: altura desde el piso a la base del mueble (altura de los tacos) en mm
    " grosor_mdf: calibre del MDF en mm
    "
    " +-----+-----+ 
    " |     |     | 
    " +-----+-----+ 
    " |     |     |
    " |    *|*    |
    " |     |     |
    " +-----+-----+
    " |           | 
    "
    """
    piezas = list()
    #
    # tabla
    #
    largo_tabla = largo
    prof_tabla = prof + 20
    tabla = carpinteria.crear_tabla(
        f"{nombre}_tabla",
        largo=largo_tabla,
        ancho=prof_tabla,
        grosor=grosor_finger,
        material="FINGER",
        color=carpinteria.COLOR_FINGER,
    )

    x_tabla = 0
    y_tabla = -10
    z_tabla = alto - grosor_finger
    tabla.trasladar(x_tabla, y_tabla, z_tabla)
    piezas.append(tabla)
    #
    # bandeja
    #
    bandeja = carpinteria.crear_placa(
        f"{nombre}_bandeja", 
        "MDF",
        largo=largo - 2*grosor_mdf,
        ancho=prof,
        grosor = grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=0,canto_der=0,
        color=color
    )
    x_bandeja = grosor_mdf
    y_bandeja = 0
    z_bandeja = alto - 2*grosor_mdf - h_bandeja
    bandeja.trasladar(x_bandeja, y_bandeja, z_bandeja)
    piezas.append(bandeja)
    #
    # base
    #
    base = carpinteria.crear_placa(
        f"{nombre}_tapa", 
        "MDF",
        largo=largo,
        ancho=prof,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=1,canto_der=1,
        color=color
    )
    x_base = x_tabla
    y_base = 0
    base.trasladar(x_base, y_base, z_base)
    piezas.append(base)
    #
    # lados
    #
    y_lado = 0
    z_lado = z_base + grosor_mdf
    prof_lado = prof
    alto_lado = alto - 2*grosor_mdf - z_base
    x_lado_izq = grosor_mdf
    lado = carpinteria.crear_placa(
        f"{nombre}_lado_izq", 
        "MDF",
        largo=alto_lado,
        ancho=prof_lado,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=0,canto_der=0,
        color=color
    )
    lado.rotar(0,-90,0)        
    lado.trasladar(x_lado_izq, y_lado, z_lado)
    piezas.append(lado)

    x_lado_der = largo 
    lado = carpinteria.crear_placa(
        f"{nombre}_lado_der", 
        "MDF",
        largo=alto_lado,
        ancho=prof_lado,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=0,canto_der=0,
        color=color
    )
    lado.rotar(0,-90,0)        
    lado.trasladar(x_lado_der,y_lado,z_lado)
    piezas.append(lado)

    #
    # divisiones
    #
    nh = 2
    #
    # divisiones de arriba (cortos)
    #
    x_div = grosor_mdf
    y_div = 0 
    z_div_c    = alto - grosor_mdf - h_bandeja
    prof_div   = prof
    alto_div_c = h_bandeja
    z_div_l    = z_base + grosor_mdf
    alto_div_l = alto - h_bandeja - z_base - 3*grosor_mdf
    dx_lado = (largo - grosor_mdf) // nh
    print(dx_lado*nh + grosor_mdf)
    x_div = grosor_mdf + dx_lado
    divc = carpinteria.crear_placa(
        f"{nombre}_divc", 
        "MDF",
        largo=alto_div_c,
        ancho=prof_div,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=0,canto_der=0,
        color=color
    )
    divc.rotar(0,-90,0)        
    divc.trasladar(x_div, y_div, z_div_c)
    piezas.append(divc)
#
    # divisiones largas
    # la segunda queda más atrás por las puertas corredizas
    x_div = grosor_mdf + dx_lado
    divl = carpinteria.crear_placa(
        f"{nombre}_divl", 
        "MDF",
        largo=alto_div_l,
        ancho=prof_div,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=0,canto_der=0,
        color=color
    )
    divl.rotar(0,-90,0)        
    divl.trasladar(x_div, y_div, z_div_l)
    piezas.append(divl)
    #
    # puertas 
    #
    x_pue = grosor_mdf - 5
    y_pue = 0
    z_pue = z_base + grosor_mdf - 5
    alto_pue = alto_div_l + 10
    ancho_pue = dx_lado - grosor_mdf + 10
    pue = carpinteria.crear_placa(
        f"{nombre}_pue_izq", 
        "MDF",
        largo=ancho_pue,
        ancho=alto_pue,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=1,canto_izq=1,canto_der=1,
        color=color
    )
    pue.rotar(90,0,0)        
    pue.trasladar(x_pue, y_pue, z_pue)
    piezas.append(pue)
    x_pue += dx_lado
    pue = carpinteria.crear_placa(
        f"{nombre}_pue_der", 
        "MDF",
        largo=ancho_pue,
        ancho=alto_pue,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=1,canto_izq=1,canto_der=1,
        color=color
    )
    pue.rotar(90,0,0)        
    pue.trasladar(x_pue, y_pue, z_pue)
    piezas.append(pue)

    
    """
def agregar_cajon(
    objetos,
    piezas,
    nombre,
    ancla,
    ancho,
    alto,
    profundidad,
    margen_vert=10,
    margen_horiz=10,
    grosor_placa=15,
    grosor_frente=18,
    grosor_guia=13,
    ancho_guia=40,
    color_frente=cq.Color("antiquewhite"),
    color_base=cq.Color("cornsilk1"),
    color_lado=cq.Color("White"),
    color_guia=cq.Color("Azure2"),
):
"""
    #
    # puertas
    #
    """
    ancho_fondo = largo - 2 * margen 
    alto_fondo = alto_lado - margen
    fondo = carpinteria.crear_placa(
        f"{nombre}_fon","MDF",
        ancho=alto_fondo,
        largo=ancho_fondo,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=1,canto_der=1,
        color=color      
    )
    fondo.rotar(90,0,0)
    fondo.trasladar(0, prof_lado + 2*grosor_mdf, margen)
    piezas.append(fondo)
    """
    return piezas

if __name__ == "__main__":
    print("COMODA")
    ancho = 400
    alto  = 600
    prof  = 400
    margen = 10
    piezas = comoda("cmd")
    ass = carpinteria.ensamblar(piezas)
    ass.add(cq.Workplane().sphere(5))
    vis.show(ass,title="COMODA")
