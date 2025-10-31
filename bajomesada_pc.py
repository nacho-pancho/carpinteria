#!/usr/bin/env python3
# 
import numpy as np
import cadquery as cq
import cadquery.vis as vis
import carpinteria
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
    x_cajon = 0
    y_cajon = 0
    for j in range(3):
        z_cajon = np.sum(np.array(altos))
        for i in range(3):
            z_cajon -= altos[i]
            cajon = carpinteria.crear_cajon(
                f"{nombre}_caj_{i}{j}",                                        
                ancho=anchos[j],
                alto=altos[i]-guarda_vert,
                profundidad=prof,
                margen_horiz=grosor_placa//2-2,
                color_base=carpinteria.COLOR_BLANCO,
                color_frente=carpinteria.COLOR_DEBUG1)
            carpinteria.trasladar(cajon,x_cajon,y_cajon,z_cajon)
            piezas.extend(cajon)
        x_cajon += huecos[j] + grosor_placa

    return piezas    
    


if __name__ == "__main__":
    print("COMODA")
    ancho = 400
    alto  = 600
    prof  = 400
    margen = 10
    piezas = bajomesada("cmd")
    ass = carpinteria.ensamblar(piezas)
    ass.add(cq.Workplane().sphere(5))
    vis.show(ass,title="COMODA")
