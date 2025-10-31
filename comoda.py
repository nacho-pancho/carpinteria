#!/usr/bin/env python3
#
# -*- coding:utf-8 -*-
# 

import numpy as np

import cadquery as cq
import cadquery.vis as vis

import carpinteria

def comoda(nombre, 
        alto_cajones=(200,200,200,200),
        largo_cajones=(500,500),
        alto_tapa=100,
        prof=500, 
        margen=10, 
        grosor_mdf=18, 
        grosor_finger=20,
        color=carpinteria.COLOR_BLANCO
    ):
    piezas = list()
    objetos = cq.Assembly()
    #
    # tabla
    #
    nh = len(largo_cajones)
    nv = len(alto_cajones)
    largo = np.sum(np.array(largo_cajones))+grosor_mdf*(nh+1) + 2*margen
    alto  = np.sum(np.array(alto_cajones))+ alto_tapa + margen + grosor_finger
    num_lados = nh + 1

    largo_tabla = largo + 2*margen
    prof_tabla = prof
    tabla = carpinteria.crear_tabla(
        f"{nombre}_tabla",
        largo=largo_tabla,
        ancho=prof_tabla,
        grosor=grosor_finger,
        material="FINGER",
        color=carpinteria.COLOR_FINGER, 
    )
    x_tabla = -margen
    y_tabla = -margen
    z_tabla = alto-grosor_finger
    tabla.trasladar(x_tabla, y_tabla, z_tabla)
    piezas.append(tabla)
    #
    # lados
    #
    y_lado = grosor_mdf
    prof_lado = prof - 2 * margen - 2*grosor_mdf
    alto_lado = alto - grosor_finger
    x_lado = grosor_mdf
    for l in range(nh+1):
        lado = carpinteria.crear_placa(
            f"{nombre}_lado_{l}", 
            "MDF",
            largo=alto_lado,
            ancho=prof_lado,
            grosor=grosor_mdf,
            canto_aba=1,canto_arr=1,canto_izq=1,canto_der=0,
            color=color
        )
        lado.rotar(0,-90,0)        
        lado.trasladar(x_lado, y_lado, 0)
        piezas.append(lado)
        if l < nh:
            x_lado += largo_cajones[l] + grosor_mdf

    #
    # fondo
    #
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

    #
    # agregamos cajones
    #
    y_cajon = grosor_mdf
    x_cajon = grosor_mdf        
    for cj in range(nh):
        z_cajon = alto - grosor_finger 
        for ci in range(nv):
            alto_hueco = alto_cajones[ci]
            ancho_hueco = largo_cajones[cj]
            z_cajon -= alto_hueco
            ancho_cajon = ancho_hueco
            guarda_vert = 5
            alto_cajon = alto_hueco - guarda_vert
            prof_hueco = prof_lado
            prof_cajon = prof_hueco - 10
            cajon = carpinteria.crear_cajon(
                f"{nombre}_caj_{ci}{cj}",
                ancho_cajon,
                alto_cajon,
                prof_cajon,
                margen_horiz=grosor_mdf//2-2,
                margen_vert=10,
                grosor_placa=grosor_mdf,
                color_frente=carpinteria.CQ_COLOR_MDF,
                color_lado=carpinteria.CQ_COLOR_MDF,
                color_base=carpinteria.CQ_COLOR_MDF,
            )
            carpinteria.trasladar(cajon,x_cajon, y_cajon, z_cajon)
            piezas.extend(cajon)
        x_cajon += ancho_hueco + grosor_mdf
    #
    # tapa
    #
    z_tapa = z_cajon - alto_tapa - guarda_vert
    ancho_tapa = largo - 2 * margen 
    tapa = carpinteria.crear_placa(
        f"{nombre}_tapa", "MDF",
        ancho=alto_tapa,
        largo=ancho_tapa,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=1,canto_der=1,canto_izq=1,
        color=color        
    )
    tapa.rotar(90,0,0)
    tapa.trasladar(0, y_lado, z_tapa)
    piezas.append(tapa)
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
