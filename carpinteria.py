#!/usr/bin/env python3 

import csv
import numpy as np
import geom
import cadquery as cq
import cadquery.vis as vis

XAXIS = cq.Vector(1,0,0)
YAXIS = cq.Vector(0,1,0)
ZAXIS = cq.Vector(0,0,1)
ZERO  = cq.Vector(0,0,0)

ALPHA = 0.7
COLOR_BLANCO = (1.0,1.0,1.0,1.0)
COLOR_MDF    = (0.5, 0.4, 0.2, ALPHA)
COLOR_FINGER = (1.0, 0.75, 0.5, ALPHA)
COLOR_GUIA   = (0.7, 0.8, 0.9, ALPHA)
COLOR_DEBUG1 = (1.0, 0.2, 0.2, ALPHA)
COLOR_DEBUG2 = (0.2, 1.0, 0.2, ALPHA)
COLOR_DEBUG3 = (0.2, 0.2, 1.0, ALPHA)
COLOR_DEBUG4 = (1.0, 1.0, 0.2, ALPHA)
COLOR_DEBUG5 = (0.2, 1.0, 1.0, ALPHA)
COLOR_DEBUG6 = (1.0, 0.2, 1.0, ALPHA)
COLOR_DEBUG7 = (1.0, 1.0, 1.0, ALPHA)

CQ_COLOR_MDF    = cq.Color(1.0, 0.975, 0.95, ALPHA)
CQ_COLOR_FINGER = cq.Color(1.0, 0.75, 0.5, ALPHA)
CQ_COLOR_GUIA   = cq.Color(0.7, 0.8, 0.9, ALPHA)
CQ_COLOR_DEBUG1 = cq.Color(1.0, 0.2, 0.2, ALPHA)
CQ_COLOR_DEBUG2 = cq.Color(0.2, 1.0, 0.2, ALPHA)
CQ_COLOR_DEBUG3 = cq.Color(0.2, 0.2, 1.0, ALPHA)
CQ_COLOR_DEBUG4 = cq.Color(1.0, 1.0, 0.2, ALPHA)
CQ_COLOR_DEBUG5 = cq.Color(0.2, 1.0, 1.0, ALPHA)
CQ_COLOR_DEBUG6 = cq.Color(1.0, 0.2, 1.0, ALPHA)
CQ_COLOR_DEBUG7 = cq.Color(1.0, 1.0, 1.0, ALPHA)


ESPESOR_CANTO=1

class Parte():
    def __init__(self, obj, loc=(0,0,0), rot=(0,0,0), color=None):
        self.obj = obj
        self.loc = loc
        self.rot = rot
        self.color = color

    def trasladar(self,dx,dy,dz):
        self.loc = geom.trans(self.loc,dx,dy,dz)
            
    def rotar(self,rx,ry,rz):
        self.loc = geom.rot(self.loc,rx,ry,rz)
        self.rot = (self.rot[0] + rx, self.rot[1] + ry, self.rot[2] + rz)


class Pieza():
    def __init__(self,desc,material):
        self.desc = desc
        self.material = material
        self.partes = list[Parte]
        self.color = (1,0,0,1)

    def agregar_parte(self,parte:Parte):
        self.partes.append(parte)

    def trasladar(self,dx,dy,dz):
        for p in self.partes:
            p.trasladar(dx,dy,dz)

    def rotar(self,rx,ry,rz):
        for p in self.partes:
            p.rotar(rx,ry,rz)


def crear_caja(largo,ancho,grosor,color):
    return Parte(cq.Workplane("XY").box(largo,ancho,grosor),color=color)


class Tabla(Pieza):
    def __init__(self,desc,material,largo,ancho,grosor,color):
        super().__init__(desc,material)
        self.ancho = ancho
        self.largo = largo
        self.grosor = grosor
        # aparece acostada, a lo largo de X, centrada en (0,0,0)
        self.partes = [crear_caja(largo,ancho,grosor,color)]



class Placa(Tabla):
    def __init__(self,
                 desc,
                 material,
                 largo,
                 ancho,
                 grosor,
                 canto_arr,
                 canto_aba,
                 canto_izq,
                 canto_der,
                 color=COLOR_BLANCO
                 ):
        super().__init__(desc,material,ancho,largo,grosor,COLOR_MDF)
        self.canto_arr = canto_arr
        self.canto_aba = canto_aba
        self.canto_izq = canto_izq
        self.canto_der = canto_der

        if canto_izq:
            largo -= 1
        if canto_der:
            largo -= 1
        if canto_aba:
            ancho -= 1
        if canto_arr:
           ancho -= 1
        #        
        self.partes = list()
        self.partes.append(crear_caja(largo,ancho,grosor-2*ESPESOR_CANTO,COLOR_MDF))
        tapa_1 = crear_caja(largo,ancho,ESPESOR_CANTO,color)
        tapa_1.trasladar(0,0,grosor/2-ESPESOR_CANTO/2)
        self.partes.append(tapa_1)
        tapa_2 = crear_caja(largo,ancho,ESPESOR_CANTO,color)
        tapa_2.trasladar(0,0,-grosor/2+ESPESOR_CANTO/2)
        self.partes.append(tapa_2)

        if canto_arr:
            canto = crear_caja(largo,ESPESOR_CANTO,grosor,color)
            canto.trasladar(0, ancho/2+ESPESOR_CANTO/2, 0)
            self.partes.append(canto)            
        if canto_aba:
            canto = crear_caja(largo,ESPESOR_CANTO,grosor,color)
            canto.trasladar(0,-ancho/2-ESPESOR_CANTO/2, 0)
            self.partes.append(canto)
        if canto_izq:
            canto = crear_caja(ESPESOR_CANTO,ancho,grosor,color)
            canto.trasladar(-largo/2-ESPESOR_CANTO/2, 0, 0)
            self.partes.append(canto)            
        if canto_der:
            canto = crear_caja(ESPESOR_CANTO,ancho,grosor,color)
            canto.trasladar( largo/2+ESPESOR_CANTO/2, 0, 0)
            self.partes.append(canto)


class Guia(Pieza):
    def __init__(self,desc,largo,ancho,grosor,color=COLOR_GUIA):
        super().__init__(desc,"GUIA")
        self.ancho = ancho
        self.largo = largo
        self.grosor = grosor
        obj = cq.Workplane("XY").box(largo,ancho,grosor).edges("|X").fillet(3)
        parte = Parte(obj,color=color)
        self.partes = [parte]

def rotar(obj,rx,ry,rz):
    if isinstance(obj,Parte):
        obj.rotar(rx,ry,rz)
    elif isinstance(obj,Pieza):
        obj.rotar(rx,ry,rz)
    elif isinstance(obj,list):
        for p in obj:
            rotar(p,rx,ry,rz)


def trasladar(obj,dx,dy,dz):
    if isinstance(obj,Parte):
        obj.trasladar(dx,dy,dz)
    elif isinstance(obj,Pieza):
        obj.trasladar(dx,dy,dz)
    elif isinstance(obj,list):
        for p in obj:
            trasladar(p,dx,dy,dz)


def ensamblar(piezas):
    res = cq.Assembly()
    for P in piezas:
        for p in P.partes:
            obj = p.obj.rotate(ZERO,XAXIS,p.rot[0])
            obj = obj.rotate(ZERO,YAXIS,p.rot[1])
            obj = obj.rotate(ZERO,ZAXIS,p.rot[2])
            res.add(obj,loc=cq.Location(p.loc),color=cq.Color(*p.color))
    return res


def crear_tabla(desc,material,largo,ancho,grosor,color):
    tabla =Tabla(desc,material,largo,ancho,grosor,color)
    tabla.trasladar(largo/2,ancho/2,grosor/2)
    return tabla

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
        #print("material",id_material)
        with open(f'{id_material}.csv','w') as f:
            for id_pieza in lista_de_piezas: # piezas de mismo tipo
                #print("pieza",id_pieza)
                pieza = lista_de_piezas[id_pieza]
                p_dim1 = pieza["dim1"]
                p_dim2 = pieza["dim2"]
                cant = len(pieza["piezas"])
                p_nombre = pieza["piezas"][0]
                rota = 1
                canto_arr = 0
                canto_aba = 0
                canto_izq = 0
                canto_der = 0
                print(f"{cant}\t{p_dim1}\t{p_dim2}\t{p_nombre}\t{rota}\t{canto_arr}\t{canto_aba}\t{canto_izq}\t{canto_der}",file=f)


def crear_placa(desc,material,largo,ancho,grosor,canto_arr,canto_aba,canto_izq,canto_der,color):
    placa = Placa(desc,material,largo,ancho,grosor,canto_arr,canto_aba,canto_izq,canto_der,color)
    placa.trasladar(largo/2,ancho/2,grosor/2)
    return placa

def crear_cajon(
    nombre,
    ancho,
    alto,
    profundidad,
    margen_vert=10,
    margen_horiz=10,
    grosor_placa=15,
    grosor_frente=18,
    grosor_guia=13,
    ancho_guia=40,
    color_frente=COLOR_BLANCO,
    color_base=COLOR_BLANCO,
    color_lado=COLOR_BLANCO,
    color_guia=COLOR_GUIA
):
    """
    " Agrega un cajon a la lista de objetos y piezas de un modelo
    " nombre : nombre 
    " ancho: ancho exterior del cajón (sin contar márgenes)
    " alto:  altura exterior del cajón  (sin contar márgenes)
    " profundidad: profundidad exterior del hueco
    " margen_vert: margen adicional de la tapa hacia arriba y abajo
    " margen_horiz: margen adicional de la tapa hacia los lados
    " grosor_placa: grosor de placa MDF de la estructura (defectio 15mm)
    " grosor_frente: grosor de la tapa de frente (ej. 18 mm)
    " grosor_guia: grosor de la guia metálica / corredera. Esta es la medida más común
    " color_frente: objeto de tipo cq.Color
    " color_base: idem 
    " color_lado: idem
    " color_guia: idem
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

    piezas = list()
    #
    # piezas
    #

    fondo = crear_placa(
        f"{nombre}_fon",
        "MDF",
        ancho_fondo, # esto es el largo 
        alto_fondo,  # esto es el ancho 
        grosor_placa, # esto es asi nomas
        canto_arr=1,
        canto_aba=0,
        canto_izq=0,
        canto_der=0,
        color=COLOR_BLANCO
    )
    fondo.rotar(90,0,0)
    fondo.trasladar(
            grosor_guia + grosor_placa,
            prof_base,
            grosor_placa + margen_vert,
        )
    piezas.append(fondo)

    frente = crear_placa(
        f"{nombre}_fre",
        "MDF",
        ancho_frente,
        alto_frente,
        grosor_frente,
        canto_arr=1,
        canto_aba=1,
        canto_izq=1,
        canto_der=1,
        color=COLOR_BLANCO
    )
    frente.rotar(90,0,0)
    frente.trasladar(-margen_horiz,0, 0)
    piezas.append(frente)

    lado_izq = crear_placa(
        f"{nombre}_lado_izq",
        "MDF",
        prof_lado,
        alto_lado,
        grosor_placa,
        canto_arr=1,
        canto_aba=1,
        canto_izq=0,
        canto_der=1,
        color=COLOR_BLANCO
    )
    lado_izq.rotar(90,0,90)    
    lado_izq.trasladar(grosor_guia, 0, margen_vert)
    piezas.append(lado_izq)

    lado_der = crear_placa(
        f"{nombre}_lado_der",
        "MDF",
        prof_lado,
        alto_lado,
        grosor_placa,
        canto_arr=1,
        canto_aba=1,
        canto_izq=0,
        canto_der=1,
        color=COLOR_BLANCO
    )
    lado_der.rotar(90,0,90)
    lado_der.trasladar(ancho_base + grosor_guia + grosor_placa, 0, margen_vert)
    piezas.append(lado_der)

    base = crear_placa(
        f"{nombre}_base",
        "MDF",
        ancho_base,
        prof_base,
        grosor_placa,        
        canto_arr=1,
        canto_aba=0,
        canto_izq=0,
        canto_der=0,
        color=COLOR_BLANCO
    )
    base.trasladar(grosor_guia + grosor_placa, 0, margen_vert)
    piezas.append(base)

    guia_izq = Guia(
        f"{nombre}_guia_izq", 
        largo_guia,
        ancho_guia,
        grosor_guia)
    guia_izq.trasladar(largo_guia/2,ancho_guia/2,grosor_guia/2)
    guia_izq.rotar(90,0,90)
    guia_izq.trasladar(0, 0, 50)
    piezas.append(guia_izq)

    guia_der = Guia(
        f"{nombre}_guia_der", 
        largo_guia,
        ancho_guia,
        grosor_guia)
    guia_der.trasladar(largo_guia/2,ancho_guia/2,grosor_guia/2)
    guia_der.rotar(90,0,90)
    guia_der.trasladar(ancho_base + grosor_guia + 2 * +grosor_placa, 0, 50)
    piezas.append(guia_der)

    return piezas


if __name__ == "__main__":
    #placa = Placa("una_placa","MDF",200,100,20,1,0,1,0,color=COLOR_BLANCO)
    #placa.trasladar(100,50,10)
    #placa.rotar(0,0,30)
    #piezas = [placa]

    cajon1 = crear_cajon("cajon",400,200,500)
    trasladar(cajon1,0,0,000)
    cajon2 = crear_cajon("cajon",400,200,500)
    trasladar(cajon2,0,0,205)
    piezas = list()
    piezas.extend(cajon1)
    piezas.extend(cajon2)
    ass = ensamblar(piezas)
    ass.add(cq.Workplane().sphere(5))
    vis.show(ass)