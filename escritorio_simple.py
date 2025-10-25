#!/usr/bin/env python3

import cadquery as cq
import cadquery.vis as vis

import carpinteria
import cajon

def escritorio_simple(
    nombre,
    largo,
    ancho,
    alto,
    alto_rack,
    ancho_rack,
    alto_cajonera,
    ancho_cajonera,
    num_cajones=4,
    margen=40,
    grosor_mdf=18,
    grosor_finger=20,
    color=carpinteria.COLOR_BLANCO
):
    piezas = list()
    #
    # tabla
    #
    z_tabla = alto
    tabla = carpinteria.crear_tabla(
        f"{nombre}_tabla",
        "FINGER",
        largo,
        ancho,
        grosor_finger,
        color=carpinteria.COLOR_FINGER
    )
    tabla.trasladar(-margen,-margen,z_tabla)
    piezas.append(tabla)
    #
    # lados
    #
    x_lado     = grosor_mdf
    y_lado     = grosor_mdf
    z_lado     = 0
    alto_lado  = alto - grosor_finger
    ancho_lado = ancho - 2 * margen - grosor_mdf

    lado_izq = carpinteria.crear_placa(
        f"{nombre}_lado_izq",
        "MDF",
         largo=alto,
         ancho=ancho_lado,
         grosor=grosor_mdf,
         canto_aba=1,canto_arr=1,canto_izq=1,
         canto_der=0,
         color=color)
    lado_izq.rotar(0,-90,0)
    lado_izq.trasladar(x_lado,y_lado,z_lado)
    piezas.append(lado_izq)

    x_lado = largo-2*margen
    lado_der = carpinteria.crear_placa(
        f"{nombre}_lado_der",
        "MDF",
         largo=alto,
         ancho=ancho_lado,
         grosor=grosor_mdf,
         canto_aba=1,canto_arr=1,canto_izq=1,
         canto_der=0,
         color=color)
    lado_der.rotar(0,-90,0)
    lado_der.trasladar(x_lado,y_lado,z_lado)
    piezas.append(lado_der)

    x_lado = 2*grosor_mdf + ancho_cajonera
    prof_cajonera = ancho_lado - ancho_rack - grosor_mdf # 1cm de holgura al fondo
    lado_med = carpinteria.crear_placa(
        f"{nombre}_lado_med",
        "MDF",
        largo=alto,
        ancho=prof_cajonera,
        grosor=grosor_mdf,
        canto_arr=1,canto_aba=1,canto_izq=1,canto_der=0,
        color=color
    )
    lado_med.rotar(0,-90,0)
    lado_med.trasladar(x_lado,y_lado,z_lado)
    piezas.append(lado_med)
    #
    # rack
    #
    largo_rack = largo - 2 * grosor_mdf - 2 * margen
    x_rack = grosor_mdf
    y_rack = ancho_lado - ancho_rack + grosor_mdf
    z_rack = alto - alto_rack
    base_rack= carpinteria.crear_placa(
        f"{nombre}_rack",
        "MDF",
        largo=largo_rack,
        ancho=ancho_rack,
        grosor=grosor_mdf,
        canto_arr=1,
        canto_aba=0,
        canto_izq=0,
        canto_der=0,
        color=color
    )
    base_rack.trasladar(x_rack,y_rack,z_rack)
    piezas.append(base_rack)
    #
    # fondo de rack
    #
    x_fondo_rack = x_rack
    y_fondo_rack = y_rack
    z_fondo_rack = z_rack 
    fondo_rack = carpinteria.crear_placa(
        f"{nombre}_fon_rack",
        material="MDF",
        largo=largo_rack,
        ancho=alto_rack,
        grosor=grosor_mdf,
        canto_arr=0,
        canto_aba=1,
        canto_izq=0,
        canto_der=0,
        color=color)
    fondo_rack.rotar(90,0,0)
    fondo_rack.trasladar(x_fondo_rack,y_fondo_rack,z_fondo_rack)
    piezas.append(fondo_rack)

    # cajones
    guarda_caj = 5
    alto_hueco_cajon = alto_cajonera // num_cajones
    alto_cajon = alto_hueco_cajon - guarda_caj
    print(alto_cajonera)
    print(alto_hueco_cajon)
    print(alto_cajon)
    prof_cajon = prof_cajonera - 10
    ancho_cajon = ancho_cajonera
    x_cajon = grosor_mdf
    y_cajon = grosor_mdf
    z_cajon = alto - alto_hueco_cajon
    for i in range(num_cajones):
        caj = carpinteria.crear_cajon(
            f"{nombre}_caj_{i}",
            ancho_cajon,
            alto_cajon,
            prof_cajon)
        carpinteria.trasladar(caj,x_cajon,y_cajon,z_cajon)
        piezas.extend(caj)
        z_cajon -= alto_hueco_cajon
    #
    # tapa de la cajonera
    #
    z_cajon += alto_hueco_cajon # deshace ultima suma innecesaria
    z_cajon -= guarda_caj       # agregamos guarda con ultimo cajon
    ancho_tapa_caj = z_cajon -margen
    largo_tapa_caj = ancho_cajonera + 2*grosor_mdf
    tapa_caj = carpinteria.crear_placa(
        f"{nombre}_tapa",
        "MDF",
        largo=largo_tapa_caj,
        ancho=ancho_tapa_caj,
        grosor=grosor_mdf,
        canto_arr=1,
        canto_aba=1,
        canto_izq=1,
        canto_der=1,
        color=color
    )
    tapa_caj.rotar(90,0,0)
    tapa_caj.trasladar(0, grosor_mdf, margen)
    piezas.append(tapa_caj)
    return piezas

    # return objetos, piezas

if __name__ == "__main__":
    margen = 10
    largo = 1000
    ancho = 600
    alto = 720
    alto_rack = 300
    prof_rack = 100
    alto_cajon = 160
    alto_cajonera = alto_cajon * 4
    ancho_cajonera = 320

    piezas = escritorio_simple(
        "es",
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
    ass = carpinteria.ensamblar(piezas)
    ass.add(cq.Workplane().sphere(5))
    vis.show(ass)
