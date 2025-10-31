#!/usr/bin/env python3
#
import cadquery.vis as vis
import carpinteria
import escritorio_con_bandeja
import escritorio_simple
import mesa_de_luz
import comoda
import bajomesada_pc

piezas = list()
# unidades en mm
#
# escritorio de esquina de 2 piezas
#
grosor_finger = 20
grosor_mdf = 18

if True:
    margen = 10
    largo = 1600
    ancho = 600
    alto = 720
    alto_rack = 300
    prof_rack = 100
    alto_cajon = 160
    alto_cajonera = alto_cajon * 4
    ancho_cajonera = 400
    prof_bandeja = 300
    ancho_bandeja = 80
    alto_bandeja = 690

    p = escritorio_con_bandeja.escritorio_con_bandeja(
        "enac",
        largo,
        ancho,
        alto,
        alto_rack,
        prof_rack,
        alto_cajonera,
        ancho_cajonera,
        ancho_bandeja=ancho_bandeja,
        alto_bandeja=alto_bandeja,
        prof_bandeja=prof_bandeja,
        margen=margen,
        grosor_mdf=18,
        grosor_finger=20
    )
    ass = carpinteria.ensamblar(p)
    #ass.add(cq.Workplane().sphere(5))
    vis.show(ass,title="ESCRITORIO NACHO")
    piezas.extend(p)

if True:
    print("ESCRITORIO DE VIOLE")
    margen = 10
    largo = 1000
    ancho = 600
    alto = 720
    alto_rack = 300
    prof_rack = 100
    alto_cajon = 160
    alto_cajonera = alto_cajon * 4
    ancho_cajonera = 320
    p = escritorio_simple.escritorio_simple(
        "evio",
        largo,
        ancho,
        alto,
        alto_rack,
        prof_rack,
        alto_cajonera,
        ancho_cajonera,
        margen=margen,
        grosor_mdf=18,
        grosor_finger=20
    )

    ass = carpinteria.ensamblar(p)
    vis.show(ass,title="ESCRITORIO VIOLE")
    piezas.extend(p)


if True:
    print("COMODA")
    ancho = 400
    alto  = 600
    prof  = 400
    margen = 10
    p = comoda.comoda("cmd")
    ass = carpinteria.ensamblar(p)
    vis.show(ass,title="COMODA")
    piezas.extend(p)

if True:
    print("BAJOMESADA PC")
    p = bajomesada_pc.bajomesada()
    ass = carpinteria.ensamblar(p)
    vis.show(ass,title="BAJOMESADA")
    piezas.extend(p)

if False:
    print("MESA DE LUZ")
    ancho = 400
    alto  = 600
    prof  = 400
    margen = 10
    alto_tapa = 100
    res, pie = mesa_de_luz.mesa_de_luz("mluz",ancho,alto,prof,alto_tapa=alto_tapa, margen=margen)
    vis.show(res,title="MESA DELUZ")
    piezas.extend(pie)

print("TODAS LAS PIEZAS")
carpinteria.lista(piezas)

# show_object(res,name="www")
carpinteria.exportar_barraca_parana(piezas)
