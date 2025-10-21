import cadquery as cq
import cadquery.vis as vis

import carpinteria
import cajon

color_mdf = cq.Color("white")
color_fin = cq.Color("antiquewhite")


def escritorio(
    ancho_ppal,
    alto_ppal,
    prof_ppal,
    alto_fondo_ppal,
    ancho_sec,
    alto_sec,
    prof_sec,
    alto_fondo_sec,
    ancho_cajones,
    margen=40,
    grosor_mdf=18,
    grosor_finger=20,
):
    prof_bandeja = 100
    pies = list()
    obj = cq.Assembly()
    #
    # tabla ppal
    #
    tabla_ppal, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=ancho_ppal,
        largo=prof_ppal,
        grosor=grosor_finger,
        material="FIN",
        nombre="tabla_ppal",
    )
    tabla_ppal = tabla_ppal.translate((0, 0, alto_ppal))
    obj = obj.add(tabla_ppal, color=color_fin)
    pies.append(pie)
    #
    # lados
    #
    lado_ppal_izq, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_ppal,
        largo=prof_ppal - 2 * margen,
        grosor=grosor_mdf,
        material="MDF",
        nombre="lado_ppal",
    )
    lado_ppal_izq = lado_ppal_izq.translate((margen, margen, 0))
    obj = obj.add(lado_ppal_izq, color=color_mdf)
    pies.append(pie)

    lado_ppal_der = lado_ppal_izq.translate(
        (ancho_ppal - 2 * margen - grosor_mdf, 0, 0)
    )
    pies.append(pie)
    obj = obj.add(lado_ppal_der, color=color_mdf)
    #
    # fondo
    #
    fondo_ppal, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_fondo_ppal,
        largo=ancho_ppal - 2 * grosor_mdf - 2 * margen,
        grosor=grosor_mdf,
        material="MDF",
        nombre="fondo_ppal",
    )
    pies.append(pie)
    obj.add(
        fondo_ppal.translate(
            (
                margen + grosor_mdf,
                prof_ppal - grosor_mdf - prof_bandeja - margen,
                alto_ppal - alto_fondo_ppal,
            )
        ),
        color=color_mdf,
    )
    #
    # bandeja
    #
    bandeja, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        largo=prof_bandeja,
        ancho=ancho_ppal - 2 * grosor_mdf - 2 * margen,
        grosor=grosor_mdf,
        material="MDF",
        nombre="bandeja",
    )
    obj.add(
        bandeja.translate(
            (
                margen + grosor_mdf,
                prof_ppal - prof_bandeja - margen,
                alto_ppal - alto_fondo_ppal,
            )
        ),
        color=color_mdf,
    )
    pies.append(pie)
    #
    # pieza secundaria
    #
    #
    # tabla sec
    #
    tabla_sec, pie = carpinteria.crear_placa(
        orientacion="horizontal",
        ancho=ancho_sec,
        largo=prof_sec,
        grosor=grosor_finger,
        material="FIN",
        nombre="tabla_sec",
    )
    tabla_sec = tabla_sec.translate((0, 0, alto_sec))
    pies.append(pie)
    #
    # lados
    #
    lado_sec_izq, pie = carpinteria.crear_placa(
        orientacion="lado",
        ancho=alto_sec,
        largo=prof_sec - 2 * margen,
        grosor=grosor_mdf,
        material="MDF",
        nombre="lado_sec",
    )
    lado_sec_izq = lado_sec_izq.translate((margen, margen, 0))
    pies.append(pie)

    lado_sec_der = lado_sec_izq.translate((ancho_sec - 2 * margen - grosor_mdf, 0, 0))
    pies.append(pie)

    lado_sec_med = lado_sec_der.translate((-ancho_cajones - grosor_mdf, 0, 0))
    pies.append(pie)
    #
    # fondo
    #
    ancho_fondo_sec = ancho_cajones + 2 * grosor_mdf
    fondo_sec, pie = carpinteria.crear_placa(
        orientacion="frente",
        ancho=alto_fondo_sec,
        largo=ancho_fondo_sec,
        grosor=grosor_mdf,
        material="MDF",
        nombre="fondo_sec",
    )
    fondo_sec = fondo_sec.translate(
        (
            ancho_sec - margen - ancho_fondo_sec,
            margen - grosor_mdf,
            alto_sec - alto_fondo_sec,
        )
    )
    pies.append(pie)
    #
    # rotamos y agregamos la pieza secundaria
    #

    tabla_sec = tabla_sec.rotate(carpinteria.ZERO, carpinteria.ZAXIS, -90)
    obj = obj.add(tabla_sec, color=color_fin)
    lado_sec_izq = lado_sec_izq.rotate(carpinteria.ZERO, carpinteria.ZAXIS, -90)
    obj = obj.add(lado_sec_izq, color=color_mdf)
    lado_sec_med = lado_sec_med.rotate(carpinteria.ZERO, carpinteria.ZAXIS, -90)
    obj = obj.add(lado_sec_med, color=color_mdf)
    lado_sec_der = lado_sec_der.rotate(carpinteria.ZERO, carpinteria.ZAXIS, -90)
    obj = obj.add(lado_sec_der, color=color_mdf)
    fondo_sec = fondo_sec.rotate(carpinteria.ZERO, carpinteria.ZAXIS, -90)
    obj = obj.add(fondo_sec, color=color_mdf)

    pies.append(pie)

    return obj, pies


# unidades en mm
#
# escritorio de esquina de 2 piezas
#
grosor_finger = 20
grosor_mdf = 18
alto_ppal = 750
prof_ppal = 600
ancho_ppal = 1500
alto_sec = 650
prof_sec = 500
ancho_sec = 1500
alto_fondo_ppal = 300
alto_fondo_sec = 600
ancho_cajones = 450
prof_bandeja = 100
margen = 40

res, pies = escritorio(
    ancho_ppal,
    alto_ppal,
    prof_ppal,
    alto_fondo_ppal,
    ancho_sec,
    alto_sec,
    prof_sec,
    alto_fondo_sec,
    ancho_cajones,
)
vis.show(res)
carpinteria.lista(pies)
# show_object(res,name="www")
