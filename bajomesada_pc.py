#!/usr/bin/env python3
# 
import cadquery as cq
import cadquery.vis as vis
import cajon
"""
 * Profundidad: 55cm
 * Ancho: dos de 51cm, uno de 103cm
 * Altura: 69cm (hasta el bordecito)
"""


if __name__ == "__main__":
    #
    # rellenamos los agujeros izquierda a derecha, de arriba a abajo
    #
    # los primeros dos agujeros son simples. El ultimo es mas grand epero tiene la pileta
    # así que cuenta como uno más, pero no me acuerdo qué tan ancho es

    alto_1 = 160 # para cubiertos y eso está bien
    alto_2 = 230 # para herramientas y cosas de esas
    alto_3 = 300 # para ollas, mas que bien. Entran botellas de productos de limpieza, etc, bastante altas. 
    

    ancho = 510
    prof  = 500
    grosor_placa = 15
    piezas = list()
    cajon_11,pie = cajon.crear_cajon(ancho,alto_1,prof)
    cajon_11.loc = cq.Location(0,0,alto_2+alto_3)
    piezas.extend(pie)

    cajon_12,pie = cajon.crear_cajon(ancho,alto_2,prof)
    cajon_12.loc = cq.Location(0,0,alto_3)
    piezas.extend(pie)

    cajon_13,pie = cajon.crear_cajon(ancho,alto_3,prof)
    piezas.extend(pie)


    x2 = ancho+grosor_placa
    cajon_21,pie = cajon.crear_cajon(ancho,alto_1,prof)
    cajon_21.loc = cq.Location(x2,0,alto_2+alto_3)
    piezas.extend(pie)

    cajon_22,pie = cajon.crear_cajon(ancho,alto_2,prof)
    cajon_22.loc = cq.Location(x2,0,alto_3)
    piezas.extend(pie)

    cajon_23,pie = cajon.crear_cajon(ancho,alto_3,prof)
    cajon_23.loc = cq.Location(x2,0,0)
    piezas.extend(pie)
    #
    # creo que hay menos espacio aca. Pongo ancho de 40
    #
    x3 = ancho+ancho+grosor_placa + grosor_placa+1030-400
    ancho3 = 400
    cajon_31,pie = cajon.crear_cajon(ancho3,alto_1,prof)
    cajon_31.loc = cq.Location(x3,0,alto_2+alto_3)
    piezas.extend(pie)

    cajon_32,pie = cajon.crear_cajon(ancho3,alto_2,prof)
    cajon_32.loc = cq.Location(x3,0,alto_3)
    piezas.extend(pie)

    cajon_33,pie = cajon.crear_cajon(ancho3,alto_3,prof)
    cajon_33.loc = cq.Location(x3,0,0)
    piezas.extend(pie)
    
    
    vis.show([cajon_11,cajon_12,cajon_13,cajon_21,cajon_22,cajon_23,cajon_31,cajon_32,cajon_33])
    piezas_por_tipo = dict()
    for p in piezas:
        mat    = p["material"]
        ancho  = p["ancho"]
        largo  = p["largo"]
        grosor = p["grosor"]
        nombre = p["nombre"]
        id = f"{mat} de {grosor}mm {ancho}mm x {largo}mm ({nombre})"
        if id not in piezas_por_tipo:
            piezas_por_tipo[id] = 1
        else:
            piezas_por_tipo[id] +=1
        print(p)
    for p in piezas_por_tipo.keys():
        print(piezas_por_tipo[p],p)