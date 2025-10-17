import cadquery as cq

XAXIS = cq.Vector(1,0,0)
YAXIS = cq.Vector(0,1,0)
ZAXIS = cq.Vector(0,0,1)
ZERO  = cq.Vector(0,0,0)

def crear_placa(orientacion,ancho,largo,grosor,nombre="sin_nombre",material="sin_material", 
                canto_arriba=False, 
                canto_abajo=False, 
                canto_derecha=False,
                canto_izquierda=False,
                canto_frente=False):
    """
    " Crea una pieza formada por una placa de ciertas dimensiones y grosor.
    " Se pasa la orientación para que sea más fácil ubicarla en 3D directamente, si bien 
    " la definición de orientación puede ser un poco confusa.
    " Cuando la orientación es horizontal, el ancho es la dimensión que va de lado a lado frente a nosotros (X, de izq a der),
    " el largo es la profundidad (hacia Y) y el grosor se extiende hacia el eje Z.
    " Cuando la orientación es vertical,  el ancho es el eje X, el grosor va hacia el fondo (eje Y) y el largo sube (eje Z)
    " Cuando la orientación es de lado, el ancho (X) es el grosor, el largo es la profundidad (Y) y el ancho va hacia arriba (eje Z)
    " Cuando la orientación es de frente, el largo de la pieza se extiende frente a nosotros (eje X), el ancho sube (eje Z) y la profundidad es el grosor (Y)
    """
    pie = {"nombre":nombre,"material":material,"ancho":ancho,"largo":largo,"grosor":grosor}
    if orientacion == "vertical":
        ancho = ancho
        prof  = grosor
        alto  = largo
    elif orientacion == "horizontal":
        ancho = ancho
        prof  = largo
        alto  = grosor
    elif orientacion == "frente":
        alto = ancho
        ancho  = largo
        prof = grosor
    elif orientacion == "lado":
        alto = ancho
        ancho  = grosor
        prof = largo
    obj = cq.Workplane("XY").box(ancho,prof,alto).translate((ancho/2,prof/2,alto/2))
    return obj,pie

def crear_tabla(orientacion,ancho,largo,grosor,nombre="sin_nombre",material="sin_material"):
    pie = {"nombre":nombre,"material":material,"ancho":ancho,"largo":largo,"grosor":grosor}
    if orientacion == "vertical":
        ancho = ancho
        prof  = grosor
        alto  = largo
    elif orientacion == "horizontal":
        ancho = ancho
        prof  = largo
        alto  = grosor
    elif orientacion == "frente":
        alto = ancho
        ancho  = largo
        prof = grosor
    elif orientacion == "lado":
        alto = ancho
        ancho  = grosor
        prof = largo
    obj = cq.Workplane("XY").box(ancho,prof,alto).translate((ancho/2,prof/2,alto/2))
    return obj,pie


def lista(piezas):
    """
    " Mostrar una lista de piezas, agrupadas por mismo tamaño, material y dimensiones
    """
    piezas_por_tipo = dict()
    for p in piezas:
        mat    = p["material"]
        ancho  = p["ancho"]
        largo  = p["largo"]
        grosor = p["grosor"]
        nombre = p["nombre"]
        id = f"{mat} de {grosor}mm {ancho}mm x {largo}mm ({nombre})"
        if id not in piezas_por_tipo:
            piezas_por_tipo[id] = 1
        else:
            piezas_por_tipo[id] +=1
    for p in sorted(piezas_por_tipo.keys()):
        print(piezas_por_tipo[p],p)