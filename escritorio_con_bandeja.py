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
    pies = list()
    obj = cq.Assembly()
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
    obj = obj.add(
        tabla.translate((0, 0, alto_tabla)), color=COLOR_FINGER, name=f"{nombre}_tabla"
    )
    pies.append(pie)
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

    obj = obj.add(
        lado_izq.translate((margen, margen, 0)),
        color=COLOR_MDF,
        name=f"{nombre}_lado_izq",
    )
    pies.append(pie)
    lado_der, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado",
    )

    obj = obj.add(
        lado_der.translate((ancho_tabla - margen - grosor_mdf, margen, 0)),
        color=COLOR_MDF,
        name=f"{nombre}_lado_der",
    )
    pies.append(pie)
    #
    # fondo de rack
    #
    ancho_rack = ancho_tabla - 2 * grosor_mdf - 2 * margen
    fondo_rack, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_rack,
        largo=ancho_rack,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo_rack",
    )
    pies.append(pie)
    obj.add(
        fondo_rack.translate(
            (
                margen + grosor_mdf,
                prof_tabla - grosor_mdf - prof_rack - margen,
                alto_tabla - alto_rack,
            )
        ),
        name=f"{nombre}_fondo_rack",
        color=COLOR_MDF,
    )
    #
    # rack
    #
    rack, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        largo=prof_rack,
        ancho=ancho_rack,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_rack",
    )
    obj.add(
        rack.translate(
            (
                margen + grosor_mdf,
                prof_tabla - prof_rack - margen,
                alto_tabla - alto_rack,
            )
        ),
        name=f"{nombre}_rack",
        color=COLOR_MDF,
    )
    pies.append(pie)

    # cajonera
    # lado
    prof_caj = prof_lado - prof_rack - grosor_mdf - 10 # 1cm de guarda
    lado_med, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_tabla,
        largo=prof_caj,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_cajonera",
    )
    obj.add(
        lado_med.translate((margen + ancho_cajonera + grosor_mdf, margen, 0)),
        name=f"{nombre}_lado_cajonera",
        color=COLOR_MDF,
    )
    pies.append(pie)
    #
    # base
    #
    base_caj, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=ancho_cajonera,
        largo=prof_caj,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_base_cajonera",
    )
    obj.add(
        base_caj.translate(
            (margen + grosor_mdf, margen, alto_tabla - alto_cajonera - grosor_mdf)
        ),
        name=f"{nombre}_base_cajonera",
        color=COLOR_MDF,
    )
    pies.append(pie)
    #
    # agregamos cajones
    #
    guarda_caj = 5
    alto_cajon = alto_cajonera // num_cajones - guarda_caj
    for i in range(num_cajones):
        obj, pies = cajon.agregar_cajon(
            obj,
            pies,
            f"{nombre}_cajon_{i}",
            (
                margen + grosor_mdf,
                margen,
                alto_tabla - (i + 1) * alto_cajonera // num_cajones,
            ),
            ancho_cajonera,
            alto_cajon,
            prof_caj,
            margen_vert=10,
            margen_horiz=10,
            grosor_placa=18,
            color_frente=COLOR_MDF,
            color_lado=COLOR_MDF,
            color_base=COLOR_MDF,
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
    obj.add(
        bandeja.translate((offset_hueco + GROSOR_GUIA, margen, alto_bandeja)),
        name=f"{nombre}_bandeja",
        color=COLOR_MDF,
    )
    pies.append(pie)

    lado_ban_izq, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=ancho_bandeja,
        largo=prof_bandeja,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_ban_izq",
    )
    obj.add(
        lado_ban_izq.translate((offset_bandeja, margen, alto_bandeja - ancho_bandeja)),
        name=f"{nombre}_lado_ban_izq",
        color=COLOR_MDF,
    )
    pies.append(pie)

    lado_ban_der, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=ancho_bandeja,
        largo=prof_bandeja,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_ban_der",
    )
    obj.add(
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
    pies.append(pie)

    fondo_ban, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=ancho_bandeja,
        largo=largo_bandeja - 2 * grosor_mdf,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo_ban",
    )
    pies.append(pie)
    obj.add(
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
    obj.add(
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
    pies.append(pie)

    guia_der, pie = carpinteria.crear_guia(
        "lado", ancho_guia, largo_guia, grosor_guia, nombre=f"{nombre}_guia_der"
    )
    obj.add(
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
    pies.append(pie)
    #
    # restricciones
    #
    # tabla, lado_izq, lado_der, fondo, rack, lado_cajonera, base_cajonera
    return obj, pies
