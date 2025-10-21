import cadquery as cq

# import cadquery.vis as vis
import carpinteria as pz

x = cq.Vector(1, 0, 0)
y = cq.Vector(0, 1, 0)
z = cq.Vector(0, 0, 1)
xaxis = x
yaxis = y
zaxis = z


def crear_placa(
    orientacion, ancho, largo, grosor, nombre="sin_nombre", material="sin_material"
):
    pie = {
        "nombre": nombre,
        "material": material,
        "ancho": ancho,
        "largo": largo,
        "grosor": grosor,
    }
    if orientacion == "horizontal":
        ancho = ancho
        prof = largo
        alto = grosor
    elif orientacion == "frente":
        alto = largo
        ancho = ancho
        prof = grosor
    elif orientacion == "lado":
        alto = ancho
        ancho = grosor
        prof = largo
    obj = (
        cq.Workplane("XY")
        .box(ancho, prof, alto)
        .translate((ancho / 2, prof / 2, alto / 2))
    )
    return obj, pie


def crear_cajon(
    ancho,
    alto,
    profundidad,
    margen_frente=5,
    grosor_placa=15,
    grosor_guia=13,
    ancho_guia=40,
    guarda_ext=2,
    guarda_int=10,
):
    obj = cq.Assembly()
    pies = list()
    return agregar_cajon(
        obj,
        pies,
        ancho,
        alto,
        profundidad,
        margen_frente,
        grosor_placa,
        grosor_guia,
        ancho_guia,
        guarda_ext,
        guarda_int,
    )


def agregar_cajon(
    objetos,
    piezas,
    nombre,
    ancla,
    ancho,
    alto,
    profundidad,
    margen_vert=10,
    margen_horiz=10,
    grosor_placa=15,
    grosor_frente=18,
    grosor_guia=13,
    ancho_guia=40,
    color_frente=cq.Color("antiquewhite"),
    color_base=cq.Color("cornsilk1"),
    color_lado=cq.Color("White"),
    color_guia=cq.Color("Azure2"),
):
    """
    " Crea un cajón con guias telescópicas a los lados.
    " ancho: ancho del hueco del cajón
    " alto: alto del hueco del cajón
    " profundidad: profundidad del cajón
    " margen_frente: margen extra en el frente del cajón en mm
    " ancho_guia: ancho de las guias telescópicas en mm
    " Devuelve un objeto CadQuery con el cajón.
    """
    # medidas
    #
    ancho_base = ancho - 2 * grosor_guia - 2 * grosor_placa
    prof_base = profundidad
    ancho_fondo = ancho_base
    alto_frente = alto
    ancho_frente = ancho + 2 * margen_horiz
    alto_lado = alto - 2*margen_vert
    alto_fondo = alto_lado - grosor_placa
    prof_lado = prof_base
    largo_guia = (prof_base // 50) * 50
    if ancla is None:
        ancla = pz.ZERO
    #
    # piezas
    #
    fondo, pie = crear_placa(
        "frente",
        ancho_fondo,
        alto_fondo,
        grosor_placa,
        nombre=f"{nombre}_fondo",
        material="MDF",
    )
    fondo = fondo.translate(
        (
            grosor_guia + grosor_placa,
            prof_base - grosor_placa,
            grosor_placa,
        )
    )
    piezas.append(pie)
    objetos = objetos.add(
        fondo.translate(ancla), name=f"{nombre}_fondo", color=color_lado
    )

    frente, pie = crear_placa(
        "frente",
        ancho_frente,
        alto_frente,
        grosor_frente,
        nombre=f"{nombre}_frente",
        material="MDF",
    )
    frente = frente.translate((-margen_horiz, -grosor_frente, 0))
    piezas.append(pie)
    objetos = objetos.add(
        frente.translate(ancla), name=f"{nombre}_frente", color=color_frente
    )

    lado, pie = crear_placa(
        "lado",
        alto_lado,
        prof_lado,
        grosor_placa,
        nombre=f"{nombre}_lado",
        material="MDF",
    )
    lado_izq = lado.translate((grosor_guia, 0, margen_vert))
    piezas.append(pie)
    objetos = objetos.add(
        lado_izq.translate(ancla), name=f"{nombre}_lado_izq", color=color_lado
    )

    lado_der = lado.translate((ancho_base + grosor_guia + grosor_placa, 0, margen_vert))
    piezas.append(pie)
    objetos = objetos.add(
        lado_der.translate(ancla), name=f"{nombre}_lado_der", color=color_lado
    )

    base, pie = crear_placa(
        "horizontal",
        ancho_base,
        prof_base,
        grosor_placa,
        nombre=f"{nombre}_base",
        material="MDF",
    )
    base = base.translate((grosor_guia + grosor_placa, 0, margen_vert))
    piezas.append(pie)
    objetos = objetos.add(
        base.translate(ancla), name=f"{nombre}_base", color=color_base
    )

    guia_izq, pie = pz.crear_guia(
        "lado", ancho_guia, largo_guia, grosor_guia, nombre=f"{nombre}_guia_izq"
    )
    guia_izq = guia_izq.translate((0, 0, 50))
    piezas.append(pie)
    objetos = objetos.add(
        guia_izq.translate(ancla), name=f"{nombre}_guia_izq", color=color_guia
    )

    guia_der, pie = pz.crear_guia(
        "lado", ancho_guia, largo_guia, grosor_guia, nombre=f"{nombre}_guia_der"
    )
    guia_der = guia_der.translate((ancho_base + grosor_guia + 2 * +grosor_placa, 0, 50))
    piezas.append(pie)
    objetos = objetos.add(
        guia_der.translate(ancla), color=color_guia, name=f"{nombre}_guia_der"
    )

    return objetos, piezas
