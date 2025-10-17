import cadquery as cq
import cadquery.vis as vis

import piezas


# unidades en mm
#
# escritorio de esquina de 2 piezas
#
grosor_finger      = 20
grosor_mdf = 18
alto_ppal = 750
prof_ppal = 600
ancho_ppal = 1500
alto_sec = 650
prof_sec = 500
ancho_sec = 1500
alto_fondo = 300
prof_bandeja = 100
margen = 20
color_mdf = cq.Color("white")
color_fin = cq.Color("antiquewhite")
def escritorio(ancho_ppal,alto_ppal,alto_sec,prof_sec):
       prof_bandeja = 100
       pies = list()
       obj = cq.Assembly()
       #
       # tabla ppal
       #
       tabla_ppal,pie  = piezas.crear_placa(orientacion="horizontal",
                                            ancho=ancho_ppal,
                                            largo=prof_ppal, 
                                            grosor=grosor_finger,
                                            material="FIN",
                                            nombre="tabla_ppal")
       tabla_ppal = tabla_ppal.translate((0,0,alto_ppal))
       obj = obj.add(tabla_ppal,color=color_fin)
       pies.append(pie)
       # 
       # lados
       # 
       lado_ppal_izq,pie   = piezas.crear_placa(orientacion="lado",
                                                ancho=alto_ppal,
                                                largo=prof_ppal-2*margen,
                                                grosor=grosor_mdf, 
                                                material="MDF",
                                                nombre="lado_ppal")
       lado_ppal_izq = lado_ppal_izq.translate((margen,margen,0))
       obj = obj.add(lado_ppal_izq,color=color_mdf)
       pies.append(pie)
       
       lado_ppal_der = lado_ppal_izq.translate((ancho_ppal-2*margen-grosor_mdf,0,0))
       pies.append(pie)
       obj = obj.add(lado_ppal_der,color=color_mdf)
       #
       # fondo
       #
       fondo_ppal,pie   = piezas.crear_placa(orientacion="frente",
                                             ancho=alto_fondo, 
                                             largo=ancho_ppal-2*grosor_mdf-2*margen,
                                             grosor=grosor_mdf, 
                                             material="MDF",
                                             nombre="fondo_ppal")
       pies.append(pie)
       obj.add(fondo_ppal.translate((margen+grosor_mdf,prof_ppal-prof_bandeja,alto_ppal-alto_fondo)),color=color_mdf)
       #
       # bandeja
       #
       return obj, pies

res,pies = escritorio(ancho_ppal,alto_ppal,alto_sec,prof_sec)
vis.show(res)
piezas.lista(pies)
#show_object(res,name="www")


