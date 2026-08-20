#!/usr/bin/env python3
#
# -*- coding:utf-8 -*-
# 

import cadquery as cq
import cadquery.vis as vis

import carpinteria


def crear_parrilla(ancho, largo, ancho_tabla, grosor_tabla):
    #
    # marco
    #
    pies = list()
    marco_parrilla_izq, pie = carpinteria.crear_placa_cq(
        "lado",
        ancho_tabla,
        largo - grosor_tabla,
        grosor_tabla,
        "lado_parrilla",
        material="pino",
    )
    marco_parrilla_izq = marco_parrilla_izq.translate((0, grosor_tabla, 0))
    pies.append(pie)
    marco_parrilla_cen = marco_parrilla_izq.translate((ancho / 2, 0, 0))
    pies.append(pie)
    marco_parrilla_der = marco_parrilla_izq.translate((ancho - grosor_tabla, 0, 0))
    pies.append(pie)

    marco_parrilla_fre, pie = carpinteria.crear_placa_cq(
        "frente", ancho_tabla, ancho, grosor_tabla, "frente_parrilla", material="pino"
    )
    pies.append(pie)
    marco_parrilla_fon = marco_parrilla_fre.translate((0, largo, 0))
    pies.append(pie)
    parrilla = (
        marco_parrilla_izq.union(marco_parrilla_cen)
        .union(marco_parrilla_der)
        .union(marco_parrilla_fre)
        .union(marco_parrilla_fon)
    )
    #
    # tablas de la parrilla
    #
    tabla_parrilla, pie = carpinteria.crear_placa_cq(
        "horizontal",
        ancho,
        ancho_tabla,
        grosor_tabla,
        nombre="tabla_parrilla",
        material="pino",
    )
    tabla_y0 = 0
    tabla_y1 = largo - ancho_tabla
    dy = (tabla_y1 - tabla_y0) / 6
    y = tabla_y0
    for i in range(6 + 1):
        parrilla = parrilla.union(tabla_parrilla.translate((0, dy * i, ancho_tabla)))
        pies.append(pie)
    #
    # patas
    #
    return parrilla, pies


def crear_patas(ancho, largo, grosor_tabla_parrilla, alto_pata, grosor_pata):
    pies = list()
    dx = ancho / 2 - grosor_tabla_parrilla - grosor_pata / 2
    dy = largo / 2 - grosor_tabla_parrilla - grosor_pata / 2
    pata_izq_fre, pie = carpinteria.crear_tabla_cq(
        "vertical", grosor_pata, alto_pata, grosor_pata, "pata", material="pino"
    )
    pata_izq_fre = pata_izq_fre.translate(
        (grosor_tabla_parrilla, grosor_tabla_parrilla, 0)
    )
    pies.append(pie)
    pata_cen_fre = pata_izq_fre.translate((dx, 0, 0))
    pies.append(pie)
    pata_der_fre = pata_cen_fre.translate((dx, 0, 0))
    pies.append(pie)

    pata_izq_med = pata_izq_fre.translate((0, dy, 0))
    pies.append(pie)
    pata_cen_med = pata_izq_med.translate((dx, 0, 0))
    pies.append(pie)
    pata_der_med = pata_cen_med.translate((dx, 0, 0))
    pies.append(pie)

    pata_izq_fon = pata_izq_med.translate((0, dy, 0))
    pies.append(pie)
    pata_cen_fon = pata_izq_fon.translate((dx, 0, 0))
    pies.append(pie)
    pata_der_fon = pata_cen_fon.translate((dx, 0, 0))
    pies.append(pie)

    patas = (
        pata_izq_fre.union(pata_der_fre)
        .union(pata_izq_med)
        .union(pata_der_med)
        .union(pata_izq_fon)
        .union(pata_der_fon)
    )
    return patas, pies


ancho_colchon = 1400
largo_colchon = 1900
alto_colchon = 300

ancho_parrilla = ancho_colchon + 40
largo_parrilla = largo_colchon + 40
ancho_tabla = 100
grosor_tabla = 20

alto_pata = 300
grosor_pata = 60

parrilla, parr_pie = crear_parrilla(
    ancho_parrilla, largo_parrilla, ancho_tabla, grosor_tabla
)
parrilla = parrilla.translate((0, 0, alto_pata - ancho_tabla))
patas, pata_pie = crear_patas(
    ancho_parrilla, largo_parrilla, grosor_tabla, alto_pata, grosor_pata
)
color_pino = cq.Color("cornsilk1")

objs = cq.Assembly().add(parrilla, color=color_pino).add(patas, color=color_pino)
vis.show(objs)
# show_object(res,name="www")
