#!/usr/bin/env python3
#
import cadquery.vis as vis
import carpinteria
import escritorio_con_bandeja
import escritorio_simple

piezas = list()
# unidades en mm
#
# escritorio de esquina de 2 piezas
#
grosor_finger = 20
grosor_mdf = 18

if False:
    alto_tabla = 790
    prof_tabla = 600
    ancho_tabla = 1600
    alto_rack = 300
    prof_rack = 100
    prof_bandeja = 300
    ancho_bandeja = 80
    alto_bandeja = 690
    alto_cajon = 160
    alto_cajonera = alto_cajon * 4
    ancho_cajonera = 400
    margen = 20
    res, pies = escritorio_con_bandeja.escritorio_con_bandeja(
        "esc_nacho",
        ancho_tabla,
        alto_tabla,
        prof_tabla,
        ancho_bandeja,
        alto_bandeja,
        prof_bandeja,
        alto_rack,
        prof_rack,
        alto_cajonera,
        ancho_cajonera,
        margen=margen,
        grosor_mdf=18,
        grosor_finger=20,
    )
    vis.show(res)
    print("ESCRITORIO DE NACHO")
    carpinteria.lista(pies)

if False:
    print("ESCRITORIO DE VIOLE")
    alto_tabla = 720
    ancho_tabla = 1000
    ancho_cajonera = 320

    res, pies2 = escritorio_simple.escritorio_simple(
        "esc_viole",
        ancho_tabla,
        alto_tabla,
        prof_tabla,
        alto_rack,
        prof_rack,
        alto_cajonera,
        ancho_cajonera,
        margen=margen,
        grosor_mdf=18,
        grosor_finger=20,
    )

    vis.show(res)
    carpinteria.lista(pies2)
    pies.extend(pies2)

import comoda

if True:
    ancho = 400
    alto  = 600
    prof  = 400
    margen = 10
    res, pie = comoda.comoda("comoda",ancho,alto,prof,margen)
    vis.show(res)
    piezas.extend(pie)
    
print("TODAS LAS PIEZAS")
carpinteria.lista(piezas)

# show_object(res,name="www")
carpinteria.exportar_barraca_parana(piezas)
