#!/usr/bin/env python3
# 
import numpy as np
import cadquery as cq
import carpinteria
import cajon
"""
 * Profundidad: 55cm
 * Ancho: dos de 51cm, uno de 103cm
 * Altura: 69cm (hasta el bordecito)
"""

def bajomesada(nombre='bmes'):
    #
    # rellenamos los agujeros izquierda a derecha, de arriba a abajo
    #
    # los primeros dos agujeros son simples. El ultimo es mas grand epero tiene la pileta
    # así que cuenta como uno más, pero no me acuerdo qué tan ancho es

    grosor_placa = 15
    alto_1 = 160 # para cubiertos y eso está bien
    alto_2 = 230 # para herramientas y cosas de esas
    alto_3 = 300 # para ollas, mas que bien. Entran botellas de productos de limpieza, etc, bastante altas. 
    altos = (alto_1,alto_2,alto_3)
    guarda_vert = 5
    huecos = (510,510,1030)
    anchos = (510,510,400)
    prof  = 500 - 10

    piezas = list()
    objetos = cq.Assembly()
    x_cajon = 0
    y_cajon = 0
    for j in range(3):
        z_cajon = np.sum(np.array(altos))
        for i in range(3):
            z_cajon -= altos[i]
            objetos,piezas = cajon.agregar_cajon(
                objetos, 
                piezas, 
                nombre=f"{nombre}_caj_{i}{j}",                                        
                ancla=(x_cajon,y_cajon,z_cajon),
                ancho=anchos[j],
                alto=altos[i]-guarda_vert,
                profundidad=prof,
                margen_horiz=grosor_placa//2-2,
                color_base=cq.Color(0.8,0.8,0.8,0.8),
                color_frente=cq.Color(0.7,0.3,0.3,0.1))
        x_cajon += huecos[j] + grosor_placa

    return objetos, piezas    
    
