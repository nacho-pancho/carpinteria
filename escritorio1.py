import cadquery as cq
import cadquery.vis as vis

import piezas
import cajon

color_mdf = cq.Color("white")
color_fin = cq.Color("antiquewhite")

def escritorio(ancho_tabla,
               alto_tabla,
               prof_tabla,
               alto_bandeja,
               prof_bandeja,
               alto_cajonera,
               ancho_cajonera,
               margen=40,
               grosor_mdf=18,
               grosor_finger=20):
       pies = list()
       obj = cq.Assembly()
       #
       # tabla
       #
       tabla,pie  = piezas.crear_placa(orientacion="horizontal",
                                            ancho=ancho_tabla,
                                            largo=prof_tabla, 
                                            grosor=grosor_finger,
                                            material="FIN",
                                            nombre="tabla_ppal")
       obj = obj.add(tabla.translate((0,0,alto_tabla)),color=color_fin)
       pies.append(pie)
       # 
       # lados
       # 
       prof_lado = prof_tabla - 2*margen
       print(prof_lado)
       lado,pie   = piezas.crear_placa(orientacion="lado",
                                                ancho=alto_tabla,
                                                largo=prof_lado,
                                                grosor=grosor_mdf, 
                                                material="MDF",
                                                nombre="lado_ppal")
       obj = obj.add(lado.translate((margen,margen,0)),color=color_mdf)
       pies.append(pie)

       obj = obj.add(lado.translate((ancho_tabla-margen-grosor_mdf,margen,0)),color=color_mdf)
       pies.append(pie)
       #
       # fondo de bandeja
       #
       ancho_bandeja = ancho_tabla-2*grosor_mdf-2*margen
       fondo_bandeja,pie   = piezas.crear_placa(orientacion="frente",
                                             ancho=alto_bandeja, 
                                             largo=ancho_bandeja,
                                             grosor=grosor_mdf, 
                                             material="MDF",
                                             nombre="fondo_ppal")
       pies.append(pie)
       obj.add(fondo_bandeja.translate((margen+grosor_mdf,prof_tabla-grosor_mdf-prof_bandeja-margen,alto_tabla-alto_bandeja)),
               color=color_mdf)
       #
       # bandeja
       #
       bandeja,pie   = piezas.crear_placa(orientacion="horizontal",
                                             largo=prof_bandeja, 
                                             ancho=ancho_bandeja,
                                             grosor=grosor_mdf, 
                                             material="MDF",
                                             nombre="bandeja")
       obj.add(bandeja.translate((margen+grosor_mdf,prof_tabla-prof_bandeja-margen,alto_tabla-alto_bandeja)),
               color=color_mdf)
       pies.append(pie)
       
       # cajonera
       # lado
       prof_caj = prof_lado - prof_bandeja - grosor_mdf
       lado_med,pie   = piezas.crear_placa(orientacion="lado",
                                                ancho=alto_tabla,
                                                largo=prof_caj,
                                                grosor=grosor_mdf, 
                                                material="MDF",
                                                nombre="lado_ppal")
       obj = obj.add(lado_med.translate((margen+ancho_cajonera+grosor_mdf,margen,0)),color=color_mdf)
       pies.append(pie)
       #
       # base
       # 
       base_caj,pie  = piezas.crear_placa(orientacion="horizontal",
                                            ancho=ancho_cajonera,
                                            largo=prof_caj, 
                                            grosor=grosor_finger,
                                            material="FIN",
                                            nombre="tabla_ppal")
       obj = obj.add(base_caj.translate((margen+grosor_mdf,margen,alto_tabla-alto_cajonera-grosor_mdf)),color=color_mdf)
       pies.append(pie)
       #
       # agregamos cajones
       #
       obj,pies = cajon.agregar_cajon(obj,pies,(margen+grosor_mdf,margen,alto_tabla-alto_cajonera//3),
                                      ancho_cajonera,alto_cajonera//3, prof_caj, margen_frente=20,grosor_placa=15,guarda_ext=20)
       obj,pies = cajon.agregar_cajon(obj,pies,(margen+grosor_mdf,margen,alto_tabla-2*alto_cajonera//3),
                                      ancho_cajonera,alto_cajonera//3, prof_caj, margen_frente=20,grosor_placa=15,guarda_ext=20)
       obj,pies = cajon.agregar_cajon(obj,pies,(margen+grosor_mdf,margen,alto_tabla-alto_cajonera),
                                      ancho_cajonera,alto_cajonera//3, prof_caj, margen_frente=20,grosor_placa=15,guarda_ext=20)
       return obj, pies


# unidades en mm
#
# escritorio de esquina de 2 piezas
#
grosor_finger      = 20
grosor_mdf = 18
alto_tabla = 750
prof_tabla = 600
ancho_tabla = 1500
alto_bandeja = 300
prof_bandeja = 100
alto_cajon = 180
alto_cajonera = alto_cajon*3
ancho_cajonera = 450
margen = 40

res,pies = escritorio(ancho_tabla, alto_tabla,prof_tabla,alto_bandeja,prof_bandeja,alto_cajonera,ancho_cajonera)
vis.show(res)
piezas.lista(pies)
#show_object(res,name="www")


