import cadquery as cq
import cadquery.vis as vis

x = cq.Vector(1,0,0)
y = cq.Vector(0,1,0)
z = cq.Vector(0,0,1)

def crear_caja(ancho,prof,alto,nombre="sin_nombre",material="sin_material"):
    obj = cq.Workplane("XY").box(ancho,prof,alto).translate((ancho/2,prof/2,alto/2))
    pie = {"nombre":nombre,"material":material,"ancho":ancho,"prof":prof,"alto":alto}
    return obj,pie

def crear_cajon(ancho, 
                alto, 
                profundidad, 
                margen_frente=5,
                grosor_placa=15, 
                grosor_guia=13,
                ancho_guia=40,
                guarda_ext=2,
                guarda_int=10): 
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
    ancho_base = ancho - 2 * grosor_guia - 2*grosor_placa 
    prof_base = profundidad - guarda_int
    alto_fondo = alto - grosor_placa - 2*guarda_int
    ancho_fondo = ancho_base
    alto_frente = alto - guarda_ext
    ancho_frente = ancho + 2*margen_frente
    alto_lado = alto - 2* guarda_int
    prof_lado = prof_base 
    largo_guia = (prof_base // 50)*50
    print(prof_base, largo_guia)
    #
    # piezas
    #    
    piezas = list()
    ancla = (cq.Workplane("XY").sphere(5))

    fondo,pie = crear_caja(ancho_fondo, grosor_placa, alto_fondo,nombre="fondo",material="MDF")
    fondo = fondo.translate((grosor_guia+grosor_placa,prof_base-grosor_placa,grosor_placa))
    piezas.append(pie)

    frente,pie = crear_caja(ancho_frente, grosor_placa, alto_frente,nombre="frente",material="MDF")
    frente = frente.translate((-margen_frente,-grosor_placa,0))
    piezas.append(pie)

    lado,pie = crear_caja(grosor_placa, prof_lado, alto_lado,nombre="lado",material="MDF")
    lado_izq = lado.translate((grosor_guia,0,0))
    piezas.append(pie)
    lado_der = lado.translate((ancho_base+grosor_guia+grosor_placa,0,0))
    piezas.append(pie)

    base,pie = crear_caja(ancho_base, prof_base, grosor_placa,nombre="base",material="MDF")
    base = base.translate((grosor_guia+grosor_placa,0,0))
    piezas.append(pie)

    guia_izq,pie = crear_caja(grosor_guia,largo_guia,ancho_guia,"guia",material="guia")
    guia_izq = guia_izq.translate((0,0,50))
    piezas.append(pie)

    guia_der,pie = crear_caja(grosor_guia,largo_guia,ancho_guia,nombre="guia",material="guia")
    guia_der = guia_der.translate((ancho_base+grosor_guia+2*+grosor_placa,0,50))
    piezas.append(pie)

    cajon = (cq.Assembly()
        .add(ancla,color=cq.Color("Yellow"))
        .add(fondo,color=cq.Color("White"))
        .add(frente,color=cq.Color("Red"))
        .add(lado_izq,color=cq.Color("White"))
        .add(lado_der,color=cq.Color("White"))
        .add(guia_izq,color=cq.Color("Azure2"))
        .add(guia_der,color=cq.Color("Azure2"))
        .add(base,color=cq.Color("beige"))
        )        
    return cajon,piezas

cajon,piezas = crear_cajon(400, 200, 500)
vis.show(cajon)
#show_object(cajon)