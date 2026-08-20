#!/usr/bin/env python3
#
# -*- coding:utf-8 -*-
# 

import cadquery as cq
import cadquery.vis as vis
import cajon
"""
* Profundidad: 55cm
* Altura: 87m (pero vamos a rebajarla hasta el mismo tamaño que la otra, 69cm)
* Agujeros: 4x51cm
"""
ancho = 510
prof  = 500

alto_1 = 16 # para cubiertos y eso está bien
alto_2 = 30 # para ollas, mas que bien. Entran botellas de productos de limpieza, etc, bastante altas. 
alto_3 = 23 # para herramientas y cosas de esas
#
# los disponemos de izquierda a derecha, de arriba a abajo
#
cajon_1 = cajon.crear_cajon_cq(510,alto_1,prof)
cajon_2 = cajon.crear_cajon_cq(510,alto_2,prof)
cajon_3 = cajon.crear_cajon_cq(510,alto_3,prof)
