import cadquery as cq
import cadquery.vis as vis

import carpinteria
import cajon

ALPHA = 0.5
COLOR_MDF = cq.Color(1.0, 0.95, 0.9, ALPHA)
COLOR_FINGER = cq.Color(1.0, 0.8, 0.6, ALPHA)


def escritorio(
    nombre,
    ancho_tabla,
    alto_tabla,
    prof_tabla,
    alto_bandeja,
    prof_bandeja,
    alto_cajonera,
    ancho_cajonera,
    margen=40,
    grosor_mdf=18,
    grosor_finger=20,
):
    pies = list()
    obj = cq.Assembly()
    #
    # tabla
    #
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
    # fondo de bandeja
    #
    ancho_bandeja = ancho_tabla - 2 * grosor_mdf - 2 * margen
    fondo_bandeja, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_bandeja,
        largo=ancho_bandeja,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_fondo",
    )
    pies.append(pie)
    obj.add(
        fondo_bandeja.translate(
            (
                margen + grosor_mdf,
                prof_tabla - grosor_mdf - prof_bandeja - margen,
                alto_tabla - alto_bandeja,
            )
        ),
        name=f"{nombre}_fondo",
        color=COLOR_MDF,
    )
    #
    # bandeja
    #
    bandeja, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        largo=prof_bandeja,
        ancho=ancho_bandeja,
        grosor=grosor_mdf,
        material="MDF",
        nombre=f"{nombre}_bandeja",
    )
    obj.add(
        bandeja.translate(
            (
                margen + grosor_mdf,
                prof_tabla - prof_bandeja - margen,
                alto_tabla - alto_bandeja,
            )
        ),
        name=f"{nombre}_bandeja",
        color=COLOR_MDF,
    )
    pies.append(pie)

    # cajonera
    # lado
    prof_caj = prof_lado - prof_bandeja - grosor_mdf
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
    obj, pies = cajon.agregar_cajon(
        obj,
        pies,
        f"{nombre}_cajon_arriba",
        (margen + grosor_mdf, margen, alto_tabla - alto_cajonera // 3),
        ancho_cajonera,
        alto_cajonera // 3,
        prof_caj,
        margen_frente=20,
        grosor_placa=15,
        guarda_ext=20,
        color_frente=COLOR_MDF,
        color_lado=COLOR_MDF,
        color_base=COLOR_MDF,
    )
    obj, pies = cajon.agregar_cajon(
        obj,
        pies,
        f"{nombre}_cajon_medio",
        (margen + grosor_mdf, margen, alto_tabla - 2 * alto_cajonera // 3),
        ancho_cajonera,
        alto_cajonera // 3,
        prof_caj,
        margen_frente=20,
        grosor_placa=15,
        guarda_ext=20,
        color_frente=COLOR_MDF,
        color_lado=COLOR_MDF,
        color_base=COLOR_MDF,
    )
    obj, pies = cajon.agregar_cajon(
        obj,
        pies,
        f"{nombre}_cajon_abajo",
        (margen + grosor_mdf, margen, alto_tabla - alto_cajonera),
        ancho_cajonera,
        alto_cajonera // 3,
        prof_caj,
        margen_frente=20,
        grosor_placa=15,
        guarda_ext=20,
        color_frente=COLOR_MDF,
        color_lado=COLOR_MDF,
        color_base=COLOR_MDF,
    )
    #
    # restricciones
    #
    # tabla, lado_izq, lado_der, fondo, bandeja, lado_cajonera, base_cajonera
    return obj, pies


# unidades en mm
#
# escritorio de esquina de 2 piezas
#
grosor_finger = 20
grosor_mdf = 18
alto_tabla = 750
prof_tabla = 600
ancho_tabla = 1500
alto_bandeja = 300
prof_bandeja = 100
alto_cajon = 180
alto_cajonera = alto_cajon * 3
ancho_cajonera = 450
margen = 40

res, pies = escritorio(
    "esc_nacho",
    ancho_tabla,
    alto_tabla,
    prof_tabla,
    alto_bandeja,
    prof_bandeja,
    alto_cajonera,
    ancho_cajonera,
)
vis.show(res)
print("ESCRITORIO DE NACHO")
carpinteria.lista(pies)

print("ESCRITORIO DE VIOLE")
ancho_tabla = 1100
ancho_cajonera = 360
res, pies2 = escritorio(
    "esc_viole",
    ancho_tabla,
    alto_tabla,
    prof_tabla,
    alto_bandeja,
    prof_bandeja,
    alto_cajonera,
    ancho_cajonera,
)
vis.show(res)
carpinteria.lista(pies2)

print("TODAS LAS PIEZAS")

pies.extend(pies2)
carpinteria.lista(pies)

# show_object(res,name="www")
