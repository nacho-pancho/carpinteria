import cadquery as cq
import cadquery.vis as vis

import carpinteria
import cajon

def escritorio_simple(
    nombre,
    ancho_tabla,
    alto_tabla,
    prof_tabla,
    alto_rack,
    prof_rack,
    alto_cajonera,
    ancho_cajonera,
    num_cajones=4,
    margen=40,
    grosor_mdf=18,
    grosor_finger=20,
):
    piezas = list()
    objetos = cq.Assembly()
    #
    # tabla
    #
    tabla, pie = carpinteria.crear_placa_cq(
        orientacion="horizontal",
        ancho=ancho_tabla,
        largo=prof_tabla,
        grosor=grosor_finger,
        material="FINGER",
        nombre=f"{nombre}_tabla",
    )
    objetos = objetos.add(
        tabla.translate((0, 0, alto_tabla)), 
        color=carpinteria.CQ_COLOR_FINGER, name=f"{nombre}_tabla"
    )
    piezas.append(pie)
    #
    # lados
    #
    y_lado = margen + grosor_mdf
    prof_lado = prof_tabla - 2 * margen - grosor_mdf
    lado_izq, pie = carpinteria.crear_placa_cq(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado",
    )

    objetos = objetos.add(
        lado_izq.translate((margen, y_lado, 0)),
        color=carpinteria.CQ_COLOR_MDF,
        name=f"{nombre}_lado_izq",
    )
    piezas.append(pie)
    lado_der, pie = carpinteria.crear_placa_cq(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado",
    )

    objetos = objetos.add(
        lado_der.translate((ancho_tabla - margen - grosor_mdf, y_lado, 0)),
        color=carpinteria.CQ_COLOR_MDF,
        name=f"{nombre}_lado_der",
    )
    piezas.append(pie)
    #
    # rack
    #
    ancho_rack = ancho_tabla - 2 * grosor_mdf - 2 * margen
    x_rack = margen + grosor_mdf
    y_rack = prof_tabla - prof_rack - margen
    z_rack = alto_tabla - alto_rack
    rack, pie = carpinteria.crear_placa_cq(
        orientacion="horizontal",
        largo=prof_rack,
        ancho=ancho_rack,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_rack",
    )
    objetos.add(
        rack.translate(
            (
                x_rack,
                y_rack,
                z_rack,
            )
        ),
        name=f"{nombre}_rack",
        color=carpinteria.CQ_COLOR_DEBUG3,
    )
    piezas.append(pie)
    #
    # fondo de rack
    #
    x_fondo_rack = x_rack
    y_fondo_rack = y_rack - grosor_mdf
    z_fondo_rack = z_rack 
    fondo_rack, pie = carpinteria.crear_placa_cq(
        orientacion="frente",
        ancho=alto_rack,
        largo=ancho_rack,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo",
    )
    piezas.append(pie)
    objetos.add(
        fondo_rack.translate(
            (
                x_fondo_rack,
                y_fondo_rack,
                z_fondo_rack,
            )
        ),
        name=f"{nombre}_fondo",
        color=carpinteria.CQ_COLOR_DEBUG2,
    )

    # cajonera
    # lado
    prof_cajonera = prof_lado - prof_rack - grosor_mdf # 1cm de holgura al fondo
    lado_med, pie = carpinteria.crear_placa_cq(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_cajonera,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_caj",
    )
    objetos.add(
        lado_med.translate((margen + ancho_cajonera + grosor_mdf, y_lado, 0)),
        name=f"{nombre}_lado_caj",
        color=carpinteria.CQ_COLOR_MDF,
    )
    piezas.append(pie)
    #
    # agregamos cajones
    #
    guarda_caj = 5
    alto_hueco_cajon = alto_cajonera // num_cajones
    alto_cajon = alto_hueco_cajon - guarda_caj
    prof_cajon = prof_cajonera - 10
    ancho_cajon = ancho_cajonera
    offset_z = alto_tabla - alto_hueco_cajon
    for i in range(num_cajones):
        objetos, piezas = cajon.agregar_cajon(
            objetos,
            piezas,
            f"{nombre}_caj_{i}",
            (
                margen + grosor_mdf,
                y_lado,
                offset_z,
            ),
            ancho_cajon,
            alto_cajon,
            prof_cajon,
            margen_vert=10,
            margen_horiz=10,
            grosor_placa=18,
            color_frente=carpinteria.CQ_COLOR_MDF,
            color_lado=carpinteria.CQ_COLOR_MDF,
            color_base=carpinteria.CQ_COLOR_MDF,
        )
        offset_z -= alto_hueco_cajon
    #
    # fondo de cajonera
    #
    ancho_fondo_caj = ancho_cajonera + grosor_mdf
    alto_fondo_caj = z_fondo_rack - margen
    y_fondo_caj = y_fondo_rack
    fondo_caj, pie = carpinteria.crear_placa_cq(
        orientacion="frente",
        ancho=alto_fondo_caj,
        largo=ancho_fondo_caj,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fon_caj"
    )
    piezas.append(pie)
    objetos.add(
        fondo_caj.translate((margen+grosor_mdf, y_fondo_caj, margen)),
        name=f"{nombre}_fon_caj",
        color=carpinteria.CQ_COLOR_DEBUG1,
    )
    #
    # tapa de la cajonera
    #
    offset_z += alto_hueco_cajon
    offset_z -= guarda_caj
    alto_tapa_caj = offset_z -margen
    ancho_tapa_caj = ancho_cajonera + 2*grosor_mdf
    tapa_caj, pie = carpinteria.crear_placa_cq(
        orientacion="frente",
        ancho=alto_tapa_caj,
        largo=ancho_tapa_caj,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_tapa"
    )
    piezas.append(pie)
    objetos.add(
        tapa_caj.translate((margen, y_lado - grosor_mdf, margen)),
        name=f"{nombre}_tapa_caj",
        color=carpinteria.CQ_COLOR_MDF,
    )

    return objetos, piezas
