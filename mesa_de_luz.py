#!/usr/bin/env python3
#
# -*- coding:utf-8 -*-
# 


import cadquery as cq

import carpinteria
import cajon


def mesa_de_luz(
    nombre, ancho, alto, prof, alto_tapa=100, margen=10, grosor_mdf=18, grosor_finger=20, color=carpinteria.COLOR_BLANCO
):
    piezas = list()
    #
    # tabla
    #
    tabla = carpinteria.crear_tabla(
        f"{nombre}_tabla",
        ancho=ancho,
        largo=prof,
        grosor=grosor_finger,
        material="FINGER",
        color=carpinteria.COLOR_FINGER, 
    )
    x_tabla = -margen
    y_tabla = -margen
    z_tabla = alto-grosor_finger
    tabla.trasladar(x_tabla,y_tabla,z_tabla)    
    piezas.append(tabla)
    #
    # lados
    #
    y_lado = grosor_mdf
    x_lado = grosor_mdf
    prof_lado = prof - 2 * margen - 2*grosor_mdf
    alto_lado = alto - grosor_finger
    ancho_hueco = ancho - 2*grosor_mdf - 2*margen
    lado = carpinteria.crear_placa(
        f"{nombre}_lado_izq", 
        "MDF",
        largo=alto_lado,
        ancho=prof_lado,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=1,canto_izq=1,canto_der=0,
        color=color
    )
    lado.rotar(0,-90,0)        
    lado.trasladar(x_lado,y_lado, 0)
    piezas.append(lado)

    lado = carpinteria.crear_placa(
        f"{nombre}_lado_der", 
        "MDF",
        largo=alto_lado,
        ancho=prof_lado,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=1,canto_izq=1,canto_der=0,
        color=color
    )
    lado.rotar(0,-90,0)        
    x_lado += ancho_hueco + grosor_mdf
    lado.trasladar(x_lado,y_lado,0)
    piezas.append(lado)

    #
    # fondo
    #
    ancho_fondo = ancho - 2 * margen 
    alto_fondo = alto - grosor_finger - margen
    fondo = carpinteria.crear_placa(
        f"{nombre}_fon","MDF",
        ancho=alto_fondo,
        largo=ancho_fondo,
        grosor=grosor_mdf,
        canto_aba=1,canto_arr=0,canto_izq=1,canto_der=1,
        color=color
    )
    fondo.rotar(90,0,0)
    x_fondo = 0
    y_fondo = prof_lado + 2*grosor_mdf
    z_fondo = margen
    fondo.trasladar(x_fondo,y_fondo,z_fondo)
    piezas.append(fondo)
    # #
    # # agregamos cajones
    # #

    y_cajon = grosor_mdf
    x_cajon = grosor_mdf        
    z_cajon = alto - grosor_finger 
    nv = 3
    prof_hueco = prof_lado
    largo_cajon = prof_hueco - 10
    ancho_cajon = ancho_hueco 
    alto_hueco = ( alto_fondo - alto_tapa ) // nv
    guarda_vert = 5
    alto_cajon = alto_hueco - guarda_vert
    for ci in range(nv):
        z_cajon -= alto_hueco
        cajon = carpinteria.crear_cajon(
            f"{nombre}_caj_{ci}",
            ancho_cajon,
            alto_cajon,
            largo_cajon,
            margen_horiz=grosor_mdf//2,
            margen_vert=10,
            grosor_placa=grosor_mdf,
            color_frente=color,
            color_lado=color,
            color_base=color,
        )
        carpinteria.trasladar(cajon,x_cajon, y_cajon, z_cajon)
        piezas.extend(cajon)
    #
    # tapa
    #
    z_tapa = z_cajon - alto_tapa - guarda_vert
    ancho_tapa = ancho - 2 * margen 
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
