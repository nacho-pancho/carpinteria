import cadquery as cq
import cadquery.vis as vis

import carpinteria
import cajon

ALPHA = 0.5
COLOR_MDF = cq.Color(1.0, 0.95, 0.9, ALPHA)
COLOR_FINGER = cq.Color(1.0, 0.8, 0.6, ALPHA)
COLOR_GUIA = cq.Color(0.7, 0.8, 0.9, ALPHA)
GROSOR_GUIA = 13
ANCHO_GUIA = 40


def escritorio_con_bandeja(
    nombre,
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
    alto_tabla -= grosor_finger
    tabla, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=ancho_tabla,
        largo=prof_tabla,
        grosor=grosor_finger,
        material="FINGER",
        nombre=f"{nombre}_tabla",
    )
    objetos = objetos.add(
        tabla.translate((0, 0, alto_tabla)), color=COLOR_FINGER, name=f"{nombre}_tabla"
    )
    piezas.append(pie)
    #
    # lados
    #
    prof_lado = prof_tabla - 2 * margen
    lado_izq, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado",
    )

    objetos = objetos.add(
        lado_izq.translate((margen, margen, 0)),
        color=COLOR_MDF,
        name=f"{nombre}_lado_izq",
    )
    piezas.append(pie)
    lado_der, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado",
    )

    objetos = objetos.add(
        lado_der.translate((ancho_tabla - margen - grosor_mdf, margen, 0)),
        color=COLOR_MDF,
        name=f"{nombre}_lado_der",
    )
    piezas.append(pie)

    #
    # rack
    #
    ancho_rack = ancho_tabla - 2 * grosor_mdf - 2 * margen
    rack, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        largo=prof_rack,
        ancho=ancho_rack,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_rack",
    )
    y_rack = prof_tabla - prof_rack - margen
    z_rack = alto_tabla - alto_rack
    objetos.add(
        rack.translate(
            (
                margen + grosor_mdf,
                y_rack,
                z_rack ,
            )
        ),
        name=f"{nombre}_rack",
        color=COLOR_MDF,
    )
    piezas.append(pie)

    #
    # fondo de rack
    #
    fondo_rack, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_rack,
        largo=ancho_rack,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo_rack",
    )
    piezas.append(pie)
    y_fondo_rack = y_rack - grosor_mdf
    z_fondo_rack = z_rack
    objetos.add(
        fondo_rack.translate(
            (
                margen + grosor_mdf,
                y_fondo_rack,
                z_fondo_rack,
            )
        ),
        name=f"{nombre}_fondo_rack",
        color=COLOR_MDF,
    )
    #
    # cajonera
    #
    # lado
    #
    prof_cajonera = prof_lado - prof_rack - grosor_mdf # 1cm de guarda
    lado_med, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_cajonera,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_cajonera",
    )
    objetos.add(
        lado_med.translate((margen + ancho_cajonera + grosor_mdf, margen, 0)),
        name=f"{nombre}_lado_cajonera",
        color=COLOR_MDF,
    )
    piezas.append(pie)
    #
    # cajones
    #
    guarda_caj = 5
    alto_hueco_cajon = alto_cajonera // num_cajones
    alto_cajon = alto_hueco_cajon - - guarda_caj
    prof_cajon = prof_cajonera - 10
    ancho_cajon = ancho_cajonera
    offset_z = alto_tabla - alto_hueco_cajon
    for i in range(num_cajones):
        objetos, piezas = cajon.agregar_cajon(
            objetos,
            piezas,
            f"{nombre}_cajon_{i}",
            (
                margen + grosor_mdf,
                margen,
                offset_z,
            ),
            ancho_cajon,
            alto_cajon,
            prof_cajon,
            margen_vert=10,
            margen_horiz=10,
            grosor_placa=18,
            color_frente=COLOR_MDF,
            color_lado=COLOR_MDF,
            color_base=COLOR_MDF,
        )        
        offset_z -= alto_hueco_cajon
    #
    # fondo de cajonera
    #
    ancho_fondo_caj = ancho_cajonera + grosor_mdf
    alto_fondo_caj = z_fondo_rack - 2*margen
    y_fondo_caj = y_fondo_rack
    fondo_caj, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_fondo_caj,
        largo=ancho_fondo_caj,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo_caj"
    )
    piezas.append(pie)
    objetos.add(
        fondo_caj.translate((margen+grosor_mdf, y_fondo_caj, 2*margen)),
        name=f"{nombre}_fondo_caj",
        color=cq.Color("Blue"),#COLOR_MDF,
    )
    #
    # tapa de la cajonera
    #
    offset_z += alto_hueco_cajon
    ancho_tapa_caj = ancho_cajonera + 2*grosor_mdf
    alto_tapa_caj = offset_z - guarda_caj -2*margen
    tapa_caj, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_tapa_caj,
        largo=ancho_tapa_caj,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_tapa"
    )
    piezas.append(pie)

    objetos.add(
        tapa_caj.translate((margen, margen-grosor_mdf, 2*margen)),
        name=f"{nombre}_tapa_caj",
        color=cq.Color("Blue"),#COLOR_MDF,
    )

    #
    # bandeja
    #
    offset_hueco = margen + ancho_cajonera + 2 * grosor_mdf
    ancho_hueco = ancho_tabla - 2 * margen - 3 * grosor_mdf - ancho_cajonera
    offset_bandeja = offset_hueco + GROSOR_GUIA
    largo_bandeja = ancho_hueco - 2 * GROSOR_GUIA
    alto_bandeja -= grosor_mdf
    bandeja, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=largo_bandeja,
        largo=prof_bandeja,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_bandeja",
    )
    objetos.add(
        bandeja.translate((offset_hueco + GROSOR_GUIA, margen, alto_bandeja)),
        name=f"{nombre}_bandeja",
        color=COLOR_MDF,
    )
    piezas.append(pie)

    lado_ban_izq, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=ancho_bandeja,
        largo=prof_bandeja,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_ban_izq",
    )
    objetos.add(
        lado_ban_izq.translate((offset_bandeja, margen, alto_bandeja - ancho_bandeja)),
        name=f"{nombre}_lado_ban_izq",
        color=COLOR_MDF,
    )
    piezas.append(pie)

    lado_ban_der, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=ancho_bandeja,
        largo=prof_bandeja,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_ban_der",
    )
    objetos.add(
        lado_ban_der.translate(
            (
                offset_bandeja + largo_bandeja - grosor_mdf,
                margen,
                alto_bandeja - ancho_bandeja,
            )
        ),
        name=f"{nombre}_lado_ban_der",
        color=COLOR_MDF,
    )
    piezas.append(pie)

    fondo_ban, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=ancho_bandeja,
        largo=largo_bandeja - 2 * grosor_mdf,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo_ban",
    )
    piezas.append(pie)
    objetos.add(
        fondo_ban.translate(
            (
                offset_bandeja + grosor_mdf,
                margen + prof_bandeja - grosor_mdf,
                alto_bandeja - ancho_bandeja,
            )
        ),
        name=f"{nombre}_fondo_bandeja",
        color=COLOR_MDF,
    )

    largo_guia = (prof_bandeja // 50) * 50
    ancho_guia = ANCHO_GUIA
    grosor_guia = GROSOR_GUIA
    guia_izq, pie = carpinteria.crear_guia(
        "lado", ancho_guia, largo_guia, grosor_guia, nombre=f"{nombre}_guia_izq"
    )
    objetos.add(
        guia_izq.translate(
            (
                margen + ancho_cajonera + 2 * grosor_mdf,
                margen,
                alto_bandeja - ancho_bandeja + (ancho_bandeja - ANCHO_GUIA) // 2,
            )
        ),
        name=f"{nombre}_guia_izq",
        color=COLOR_GUIA,
    )
    piezas.append(pie)

    guia_der, pie = carpinteria.crear_guia(
        "lado", ancho_guia, largo_guia, grosor_guia, nombre=f"{nombre}_guia_der"
    )
    objetos.add(
        guia_der.translate(
            (
                margen + ancho_cajonera + 2 * grosor_mdf + GROSOR_GUIA + largo_bandeja,
                margen,
                alto_bandeja - ancho_bandeja + (ancho_bandeja - ANCHO_GUIA) // 2,
            )
        ),
        name=f"{nombre}_guia_der",
        color=COLOR_GUIA,
    )
    piezas.append(pie)
    #
    # restricciones
    #
    # tabla, lado_izq, lado_der, fondo, rack, lado_cajonera, base_cajonera
    return objetos, piezas
