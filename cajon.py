import cadquery as cq
#import cadquery.vis as vis

x = cq.Vector(1,0,0)
y = cq.Vector(0,1,0)
z = cq.Vector(0,0,1)
xaxis = x
yaxis = y
zaxis = z

def crear_placa(orientacion,ancho,largo,grosor,nombre="sin_nombre",material="sin_material", 
                canto_arriba=False, 
                canto_abajo=False, 
                canto_derecha=False,
                canto_izquierda=False,
                canto_frente=False):
    pie = {"nombre":nombre,"material":material,"ancho":ancho,"largo":largo,"grosor":grosor}
    if orientacion == "horizontal":
        ancho = ancho
        prof  = largo
        alto  = grosor
    elif orientacion == "frente":
        alto = largo
        ancho  = ancho
        prof = grosor
    elif orientacion == "lado":
        alto = ancho
        ancho  = grosor
        prof = largo
    obj = cq.Workplane("XY").box(ancho,prof,alto).translate((ancho/2,prof/2,alto/2))
    return obj,pie

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
        obj = cq.Assembly()
        pies = list()
        return agregar_cajon(obj,pies,ancho,alto,profundidad,margen_frente,grosor_placa,grosor_guia,ancho_guia,guarda_ext,guarda_int)


def agregar_cajon(objetos, 
                piezas,
                ancla,
                ancho, 
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
    ancho_fondo = ancho_base
    alto_frente = alto - guarda_ext
    ancho_frente = ancho + 2*margen_frente
    alto_lado = alto - 2*guarda_int
    alto_fondo = alto_lado - grosor_placa - guarda_int
    prof_lado = prof_base 
    largo_guia = (prof_base // 50)*50
    if ancla is None:
         ancla = piezas.ZERO
    #
    # piezas
    #    
    fondo,pie = crear_placa("frente",ancho_fondo, alto_fondo, grosor_placa,nombre="fondo_cajon",material="MDF")
    fondo = fondo.translate((grosor_guia+grosor_placa,prof_base-grosor_placa,grosor_placa+guarda_int))
    piezas.append(pie)
    objetos = objetos.add(fondo.translate(ancla),color=cq.Color("White"))

    frente,pie = crear_placa("frente",ancho_frente, alto_frente, grosor_placa, nombre="frente_cajon",material="MDF")
    frente = frente.translate((-margen_frente,-grosor_placa,0))
    piezas.append(pie)
    objetos = objetos.add(frente.translate(ancla),color=cq.Color("Red"))

    lado,pie = crear_placa("lado", alto_lado,prof_lado, grosor_placa,nombre="lado_cajon",material="MDF")
    lado_izq = lado.translate((grosor_guia,0,0))
    piezas.append(pie)
    objetos = objetos.add(lado_izq.translate(ancla),color=cq.Color("White"))

    lado_der = lado.translate((ancho_base+grosor_guia+grosor_placa,0,0))
    piezas.append(pie)
    objetos = objetos.add(lado_der.translate(ancla),color=cq.Color("White")) 

    base,pie = crear_placa("horizontal",ancho_base, prof_base, grosor_placa,nombre="base_cajon",material="MDF")
    base = base.translate((grosor_guia+grosor_placa,0,guarda_int))
    piezas.append(pie)
    objetos = objetos.add(base.translate(ancla),color=cq.Color("beige"))

    guia_izq,pie = crear_caja(grosor_guia,largo_guia,ancho_guia,nombre="guia_cajon",material="guia")
    guia_izq = guia_izq.translate((0,0,50))
    #piezas.append(pie)
    objetos = objetos.add(guia_izq.translate(ancla),color=cq.Color("Azure2"))

    guia_der,pie = crear_caja(grosor_guia,largo_guia,ancho_guia,nombre="guia_cajon",material="guia")
    guia_der = guia_der.translate((ancho_base+grosor_guia+2*+grosor_placa,0,50))
    #piezas.append(pie)
    objetos = objetos.add(guia_der.translate(ancla),color=cq.Color("Azure2"))
    
    return objetos,piezas

