from core import *

def export_parana(piezas):
    #
    # :TODO: need to adapt to new version
    #
    listas_de_materiales = dict()
    for p in piezas:
        mat    = p.material
        grosor = p.grosor
        id_material = f'{mat}_{grosor}'
        ancho  = p.ancho
        largo  = p.largo
        if isinstance(p,Placa):
            arr,aba,izq,der = p.canto_arr,p.canto_aba,p.canto_izq,p.canto_der
        else:
            arr,aba,izq,der=0,0,0,0
        id_pieza = f'{largo}x{ancho}_{arr}{aba}{izq}{der}'

        nombre = p.desc
        if id_material not in listas_de_materiales:
            lista_de_piezas = dict()
            piezas = [nombre]
            lista_de_piezas[id_pieza] = {"largo":largo,
                                         "ancho":ancho,
                                            "arr":arr,
                                            "aba":aba,
                                            "izq":izq,
                                            "der":der,
                                         "piezas":piezas}
            listas_de_materiales[id_material] = lista_de_piezas
        else:
            lista_de_piezas = listas_de_materiales[id_material]
            if id_pieza not in lista_de_piezas:
                lista_de_piezas[id_pieza] = {"largo":largo,
                                             "ancho":ancho,
                                            "arr":arr,
                                            "aba":aba,
                                            "izq":izq,
                                            "der":der,
                                            "piezas":[nombre]}
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
                p_largo = pieza["largo"]
                p_ancho = pieza["ancho"]
                cant = len(pieza["piezas"])
                p_nombre = pieza["piezas"][0]
                rota = 1
                canto_arr = pieza["arr"]
                canto_aba = pieza["aba"]
                canto_izq = pieza["izq"]
                canto_der = pieza["der"]
                print(f"{cant}\t{p_largo}\t{p_ancho}\t{p_nombre}\t{rota}\t{canto_arr}\t{canto_aba}\t{canto_izq}\t{canto_der}",file=f)

def export_gltf():
    # :TODO: would be nice to export for super high quality rendering
    # https://www.khronos.org/gltf/
    