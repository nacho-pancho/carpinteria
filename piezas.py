import cadquery as cq

XAXIS = cq.Vector(1,0,0)
YAXIS = cq.Vector(0,1,0)
ZAXIS = cq.Vector(0,0,1)
ZERO  = cq.Vector(0,0,0)

def crear_caja(ancho,prof,alto,nombre="sin_nombre",material="sin_material"):
    """
    " Crea una caja con la esquina inferior izquierda frontal en (0,0,0)
    " con el ancho (hacia X), profundidad (hacia Y), y alto (hacia Z) especificados
    """
    obj = cq.Workplane("XY").box(ancho,prof,alto).translate((ancho/2,prof/2,alto/2))
    pie = {"nombre":nombre,"material":material,"ancho":ancho,"prof":prof,"alto":alto}
    return obj,pie



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


def crear_guia(orientacion,ancho,largo,grosor,nombre):
    obj,pie = crear_placa(orientacion,ancho,largo,grosor,nombre,material="GUIA")
    obj = obj.edges("|Y").fillet(3)
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

import csv

def lista(piezas,fname='materiales.csv'):
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
        dim1 = min(ancho,largo)
        dim2 = max(ancho,largo)
        id = f"{mat:8} | {grosor:10d} | {dim1:8d} | {dim2:8d}"
        if id not in piezas_por_tipo:
            piezas_por_tipo[id] = [nombre]
        else:
            piezas_por_tipo[id].append(nombre)

    with open(fname,'w') as f:
        print("cant. | material | grosor(mm) | dim1(mm) | dim2(mm) | piezas")
        print("cant. | material | grosor(mm) | dim1(mm) | dim2(mm) | piezas",file=f)
        for p in sorted(piezas_por_tipo.keys()):
            n = len(piezas_por_tipo[p])
            lp = ','.join(piezas_por_tipo[p])
            print(f"{n:5d} | {p} | {lp}")
            print(f"{n:5d} | {p} | {lp}",file=f)
