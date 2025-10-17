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

def exportar_barraca_parana(piezas):
    listas_de_materiales = dict()
    for p in piezas:
        mat    = p["material"]
        grosor = p["grosor"]
        id_material = f'{mat}_{grosor}'
        ancho  = p["ancho"]
        largo  = p["largo"]

        dim1 = min(ancho,largo)
        dim2 = max(ancho,largo)
        id_pieza = f'{dim1}_{dim2}'

        nombre = p["nombre"]
        if id_material not in listas_de_materiales:
            lista_de_piezas = dict()
            piezas = [nombre]
            lista_de_piezas[id_pieza] = {"dim1":dim1,"dim2":dim2,"piezas":piezas}
            listas_de_materiales[id_material] = lista_de_piezas
        else:
            lista_de_piezas = listas_de_materiales[id_material]
            if id_pieza not in lista_de_piezas:
                lista_de_piezas[id_pieza] = {"dim1":dim1,"dim2":dim2,"piezas":[nombre]}
            else:
                lista_de_piezas[id_pieza]["piezas"].append(nombre)
            listas_de_materiales[id_material]= lista_de_piezas
        
    for id_material in listas_de_materiales.keys():
        lista_de_piezas = listas_de_materiales[id_material]
        print("material",id_material)
        with open(f'{id_material}.csv','w') as f:
            for id_pieza in lista_de_piezas: # piezas de mismo tipo
                print("pieza",id_pieza)
                pieza = lista_de_piezas[id_pieza]
                p_dim1 = pieza["dim1"]
                p_dim2 = pieza["dim2"]
                cant = len(pieza["piezas"])
                p_nombre = pieza["piezas"][0]
                rota = 0
                canto_arr = 0
                canto_aba = 0
                canto_izq = 0
                canto_der = 0
                print(f"{cant}\t{p_dim1}\t{p_dim2}\t{p_nombre}\t{rota}\t{canto_arr}\t{canto_aba}\t{canto_izq}\t{canto_der}",file=f)
