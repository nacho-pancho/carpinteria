import cadquery as cq

import carpinteria
import cajon


def mesa_de_luz(
    nombre, ancho, alto, prof, alto_tapa=100, margen=10, grosor_mdf=18, grosor_finger=20
):
    piezas = list()
    objetos = cq.Assembly()
    #
    # tabla
    #
    tabla, pie = carpinteria.crear_placa_cq(
        orientacion="horizontal",
        ancho=ancho,
        largo=prof,
        grosor=grosor_finger,
        material="FINGER",
        nombre=f"{nombre}_tabla",
    )
    objetos = objetos.add(
        tabla.translate((0, 0, alto-grosor_finger)), 
        color=carpinteria.CQ_COLOR_FINGER, 
        name=f"{nombre}_tabla"
    )
    piezas.append(pie)
    #
    # lados
    #
    prof_lado = prof - 2 * margen - 2*grosor_mdf
    alto_lado = alto - grosor_finger
    lado_izq, pie = carpinteria.crear_placa_cq(
        orientacion="lado",
        ancho=alto_lado,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_izq",
    )

    objetos = objetos.add(
        lado_izq.translate((margen, margen + grosor_mdf, 0)),
        color=carpinteria.CQ_COLOR_MDF,
        name=f"{nombre}_lado_izq",
    )
    piezas.append(pie)
    lado_der, pie = carpinteria.crear_placa_cq(
        orientacion="lado",
        ancho=alto_lado,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_der",
    )

    objetos = objetos.add(
        lado_der.translate((ancho - margen - grosor_mdf, margen + grosor_mdf, 0)),
        color=carpinteria.CQ_COLOR_MDF,
        name=f"{nombre}_lado_der",
    )
    piezas.append(pie)
    #
    # fondo
    #
    ancho_fondo = ancho - 2 * margen 
    alto_fondo = alto - grosor_finger - margen
    fondo, pie = carpinteria.crear_placa_cq(
        orientacion="frente",
        ancho=alto_fondo,
        largo=ancho_fondo,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo",
    )
    piezas.append(pie)
    objetos.add(
        fondo.translate((
            margen, 
            prof_lado + margen + grosor_mdf, 
            margen)),
        name=f"{nombre}_fondo",
        color=carpinteria.CQ_COLOR_MDF,
    )
    #
    # agregamos cajones
    #
    num_cajones = 3
    ancho_hueco = ancho_fondo - 2*grosor_mdf
    alto_hueco = alto - margen - grosor_finger - alto_tapa
    print(alto_tapa)
    print(alto_hueco)
    ancho_cajon = ancho_hueco
    guarda_vert = 5
    alto_hueco_cajon = alto_hueco // num_cajones 
    alto_cajon = alto_hueco_cajon - guarda_vert
    prof_hueco = prof_lado - margen
    offset_z = alto - grosor_finger - alto_hueco_cajon
    for i in range(num_cajones):
        ancla = (margen + grosor_mdf, margen + grosor_mdf, offset_z)
        objetos, piezas = cajon.agregar_cajon(
            objetos,
            piezas,
            f"{nombre}_cajon_{i}",
            ancla,
            ancho_cajon,
            alto_cajon,
            prof_hueco,
            margen_horiz=grosor_mdf,
            margen_vert=10,
            grosor_placa=grosor_mdf,
            color_frente=carpinteria.CQ_COLOR_MDF,
            color_lado=carpinteria.CQ_COLOR_MDF,
            color_base=carpinteria.CQ_COLOR_MDF,
        )
        offset_z -= alto_hueco_cajon

    #
    # tapa
    #
    
    offset_z += alto_hueco_cajon - guarda_vert
    alto_tapa = offset_z - margen
    offset_z = margen
    ancho_tapa = ancho - 2 * margen 
    tapa, pie = carpinteria.crear_placa_cq(
        orientacion="frente",
        ancho=alto_tapa,
        largo=ancho_tapa,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_tapa",
    )
    piezas.append(pie)

    objetos.add(
        tapa.translate((margen, margen, offset_z)),
        name=f"{nombre}_tapa",
        color=carpinteria.CQ_COLOR_MDF,
    )

    return objetos, piezas
