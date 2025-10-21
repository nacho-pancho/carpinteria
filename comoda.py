import cadquery as cq

import carpinteria
import cajon

ALPHA = 0.5
COLOR_MDF = cq.Color(1.0, 0.95, 0.9, ALPHA)
COLOR_FINGER = cq.Color(1.0, 0.8, 0.6, ALPHA)


def comoda(
    nombre, ancho, alto, prof, margen=10, grosor_mdf=18, grosor_finger=20
):
    pies = list()
    obj = cq.Assembly()
    #
    # tabla
    #
    tabla, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=ancho,
        largo=prof,
        grosor=grosor_finger,
        material="FINGER",
        nombre=f"{nombre}_tabla",
    )
    obj = obj.add(
        tabla.translate((0, 0, alto-grosor_finger)), color=COLOR_FINGER, name=f"{nombre}_tabla"
    )
    pies.append(pie)
    #
    # lados
    #
    prof_lado = prof - 2 * margen - grosor_mdf
    alto_lado = alto - grosor_finger
    lado_izq, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_lado,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_izq",
    )

    obj = obj.add(
        lado_izq.translate((margen, margen + grosor_mdf, 0)),
        color=COLOR_MDF,
        name=f"{nombre}_lado_izq",
    )
    pies.append(pie)
    lado_der, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_lado,
        largo=prof_lado,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_lado_der",
    )

    obj = obj.add(
        lado_der.translate((ancho - margen - grosor_mdf, margen + grosor_mdf, 0)),
        color=COLOR_MDF,
        name=f"{nombre}_lado_der",
    )
    pies.append(pie)
    #
    # fondo
    #
    ancho_fondo = ancho - 2 * margen - 2 * grosor_mdf
    alto_fondo = alto - grosor_finger - margen
    fondo, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_fondo,
        largo=ancho_fondo,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo",
    )
    pies.append(pie)
    obj.add(
        fondo.translate((margen + grosor_mdf, prof - grosor_mdf - margen, margen)),
        name=f"{nombre}_fondo",
        color=COLOR_MDF,
    )
    #
    # base
    #
    ancho_base = ancho - 2*margen - 2 * grosor_mdf
    prof_base = prof - 2*margen - 2*grosor_mdf
    base, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=ancho_base,
        largo=prof_base,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_base",
    )
    obj.add(
        base.translate((margen + grosor_mdf, margen + grosor_mdf, margen)),
        name=f"{nombre}_base",
        color=COLOR_MDF,
    )
    pies.append(pie)
    #
    # agregamos cajones
    #
    num_cajones = 3
    alto_hueco = alto - margen - grosor_finger
    ancho_hueco = ancho_base
    ancho_cajon = ancho_hueco
    guarda_vert = 5
    alto_hueco_cajon = alto_hueco // num_cajones # - guarda_vert
    alto_cajon = alto_hueco_cajon - guarda_vert
    prof_hueco = prof_base
    for i in range(num_cajones):
        ancla = (margen + grosor_mdf, margen + grosor_mdf, alto - grosor_finger - (i + 1) * alto_hueco_cajon)
        obj, pies = cajon.agregar_cajon(
            obj,
            pies,
            f"{nombre}_cajon_{i}",
            ancla,
            ancho_cajon,
            alto_cajon,
            prof_hueco,
            margen_horiz=grosor_mdf,
            margen_vert=10,
            grosor_placa=grosor_mdf,
            color_frente=COLOR_MDF,
            color_lado=COLOR_MDF,
            color_base=COLOR_MDF,
        )
    #
    # restricciones
    #
    # tabla, lado_izq, lado_der, fondo, bandeja, lado_cajonera, base_cajonera
    return obj, pies
