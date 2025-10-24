import numpy as np

import cadquery as cq

import carpinteria
import cajon

ALPHA = 0.5
COLOR_MDF = cq.Color(1.0, 0.95, 0.9, ALPHA)
COLOR_FINGER = cq.Color(1.0, 0.8, 0.6, ALPHA)


def comoda(nombre, 
        alto_cajones=(200,200,200,200),
        ancho_cajones=(500,500),
        alto_tapa=100,
        prof=500, 
        margen=10, 
        grosor_mdf=18, 
        grosor_finger=20,
    ):
    piezas = list()
    objetos = cq.Assembly()
    #
    # tabla
    #
    nh = len(ancho_cajones)
    nv = len(alto_cajones)
    ancho = np.sum(np.array(ancho_cajones))+grosor_mdf*(nh+1) + 2*margen
    alto  = np.sum(np.array(alto_cajones))+ alto_tapa + 2*margen + grosor_finger
    print(alto)
    num_lados = nh + 1
    tabla, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=ancho,
        largo=prof+2*grosor_mdf,
        grosor=grosor_finger,
        material="FINGER",
        nombre=f"{nombre}_tabla",
    )
    objetos = objetos.add(
        tabla.translate((0, -margen-grosor_mdf, alto-grosor_finger)), color=COLOR_FINGER, name=f"{nombre}_tabla"
    )
    piezas.append(pie)
    #
    # lados
    #
    prof_lado = prof - 2 * margen - grosor_mdf
    alto_lado = alto - grosor_finger
    offset_x = margen
    offset_y = margen
    for l in range(nh+1):
        lado, pie = carpinteria.crear_placa(
            orientacion="lado",
            ancho=alto_lado,
            largo=prof_lado,
            grosor=grosor_mdf,
            material="MDF",
            nombre=f"{nombre}_lado_{l}",
        )
        
        objetos = objetos.add(
            lado.translate((offset_x, offset_y, 0)),
            color=COLOR_MDF,
            name=f"{nombre}_lado_{l}",
        )
        piezas.append(pie)
        if l < nh:
            offset_x += ancho_cajones[l] + grosor_mdf

    #
    # fondo
    #
    ancho_fondo = ancho - 2 * margen 
    alto_fondo = alto - grosor_finger - margen
    fondo, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_fondo,
        largo=ancho_fondo,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo",
    )
    piezas.append(pie)
    objetos.add(
        fondo.translate((margen, prof - grosor_mdf - margen, margen)),
        name=f"{nombre}_fondo",
        color=COLOR_MDF,
    )
    #


    ancho_base = ancho - 2*margen - 2 * grosor_mdf
    prof_base = prof - 2*margen - grosor_mdf - 10
    #
    # agregamos cajones
    #
    offset_y = margen
    offset_x = margen + grosor_mdf        
    for cj in range(nh):
        offset_z = alto - grosor_finger 
        for ci in range(nv):
            alto_hueco = alto_cajones[ci]
            ancho_hueco = ancho_cajones[cj]
            offset_z -= alto_hueco
            ancho_cajon = ancho_hueco
            guarda_vert = 5
            alto_cajon = alto_hueco - guarda_vert
            prof_hueco = prof_base
            ancla = (offset_x, offset_y, offset_z)
            objetos, piezas = cajon.agregar_cajon(
                objetos,
                piezas,
                f"{nombre}_cajon_{ci}_{cj}",
                ancla,
                ancho_cajon,
                alto_cajon,
                prof_hueco,
                margen_horiz=grosor_mdf//2,
                margen_vert=10,
                grosor_placa=grosor_mdf,
                color_frente=COLOR_MDF,
                color_lado=COLOR_MDF,
                color_base=COLOR_MDF,
            )
        offset_x += ancho_hueco + grosor_mdf
    #
    # tapa
    #
    offset_z -= alto_tapa + guarda_vert
    ancho_tapa = ancho - 2 * margen 
    tapa, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_tapa,
        largo=ancho_tapa,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_tapa",
    )
    piezas.append(pie)

    objetos.add(
        tapa.translate((margen, margen-grosor_mdf, offset_z)),
        name=f"{nombre}_tapa",
        color=COLOR_MDF,
    )
    return objetos, piezas
