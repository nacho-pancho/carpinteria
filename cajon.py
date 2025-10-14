import cadquery as cq
import cadquery.vis as vis

def crear_cajon(ancho, 
                alto, 
                profundidad, 
                margen_frente=5,
                grosor_placa=15, 
                ancho_guia=13,
                altura_guia=30,
                guarda=5): 
    """
    " Crea un cajón con guias telescópicas a los lados.
    " ancho: ancho del hueco del cajón
    " alto: alto del hueco del cajón
    " profundidad: profundidad del cajón
    " margen_frente: margen extra en el frente del cajón en mm
    " ancho_guia: ancho de las guias telescópicas en mm
    " Devuelve un objeto CadQuery con el cajón.
    """
    #
    # medidas
    #
    ancho_base = ancho - 2 * ancho_guia 
    prof_base = profundidad - guarda
    alto_fondo = alto - grosor_placa - 2*guarda
    ancho_fondo = ancho_base - 2 * grosor_placa 
    alto_frente = alto - guarda
    ancho_frente = ancho + 2*margen_frente
    alto_lado = alto - 2* guarda
    prof_lado = prof_base
    #
    # piezas
    #
    fondo = (cq.Workplane("XY")
            .box(ancho_fondo, grosor_placa, alto_fondo)
            .translate((0,  prof_base / 2 - grosor_placa /2, alto_fondo/2 + grosor_placa))
            )
    frente = (cq.Workplane("XY")
            .box(ancho_frente, grosor_placa, alto_frente)
            .translate((0, -prof_base/2 + grosor_placa/2, alto_frente/2))
            )
    lado_izq = (cq.Workplane("XY")
            .box(grosor_placa, prof_lado, alto_lado)
            .translate((-ancho_base/2 + grosor_placa/2, 0, alto_lado/2))
            )
    lado_der = (cq.Workplane("XY")
            .box(grosor_placa, prof_lado, alto_lado)
            .translate((ancho_base/2 - grosor_placa/2, 0, alto_lado/2))
            )
    base = (cq.Workplane("XY")
            .box(ancho_base, prof_base, grosor_placa)
            .translate((0, 0, grosor_placa / 2))
            )
    cajon = fondo.union(frente).union(fondo).union(lado_izq).union(lado_der).union(base)
    return cajon

cajon = crear_cajon(400, 200, 500)
res = cq.Assembly().add(cajon, name="cajon",color=cq.Color(0.8,0.4,0.1,0.5))
vis.show(res)
