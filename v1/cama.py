import cadquery as cq
import cadquery.vis as vis
#
# utilidades
#
zero  = cq.Vector(0,0,0)
xaxis = cq.Vector(1,0,0)
yaxis = cq.Vector(0,1,0)
zaxis = cq.Vector(0,0,1)

# unidades en mm
#
# cama de dos plazas
#
ancho_colchon = 1400
largo_colchon = 1900
alto_colchon = 300

ancho_cama = ancho_colchon+60
largo_cama = largo_colchon+60

# medida de materiales
#
grosor_lamina      = 5# hay entre 3 y 5. Hay 9 pero es una exageracion
grosor_finger      = 20
ancho_pata         = 80 # 3 pulgadas
#
# parrilla
#
grosor_parrilla    = 40
grosor_soporte     = 20
ancho_tabla = 150
grosor_tabla = 20

# altura de la cama
# se calcula en base a varias cosas
# en mm
alto_ruedita      = 15# https://articulo.mercadolibre.com.uy/MLU-639321402-rueditas-adhesiva-giratoria-muebles-set-x4-und-_JM#polycard_client=search-nordic&search_layout=stack&position=8&type=item&tracking_id=4387314a-b7dc-45ae-b8f5-7e0ee4d4d3a3&wid=MLU639321402&sid=search
radio_ruedita     = 25


#
# 4 cajones, 2 de cada lado
#
ancho_cajon_soporte = 50 # 2 pulgadas
alto_cajon_util    = 200
alto_cajon = grosor_soporte + grosor_lamina + alto_cajon_util
margen_rueditas = 25


ancho_agujero_cajon=(largo_cama-2*grosor_finger-ancho_pata-2*ancho_pata)/2
ancho_tapa_cajon   = (largo_cama -2*grosor_finger) / 2
prof_agujero_cajon = ( ancho_cama -2*grosor_finger) / 2
prof_base_cajon    = prof_agujero_cajon - grosor_finger
ancho_base_cajon   = ancho_agujero_cajon - 2* grosor_finger 

cota_marco = alto_cajon+alto_ruedita

alto_soporte_parrilla = 100
base_colchon = alto_cajon + alto_soporte_parrilla + grosor_tabla + alto_ruedita
alto_frente = alto_cajon + alto_soporte_parrilla + grosor_tabla + 50
alto_frente_cajon = alto_frente - alto_ruedita

print("alto de frente de cama",alto_frente)
print("alto de tapa de cajon",alto_frente_cajon)
largo_parrilla = largo_cama-2*grosor_finger-2*grosor_parrilla
ancho_parrilla = ancho_cama-2*grosor_finger
alto_respaldo = alto_frente # + 100
print("alto del respaldo",alto_respaldo)

cota_tabla = base_colchon-grosor_tabla/2

#
# cajones (lo mas complicado)
#
rue1 = (cq.Workplane().
        cylinder(alto_ruedita,radio_ruedita).
        translate((-ancho_base_cajon/2 + margen_rueditas, prof_base_cajon/2-margen_rueditas, alto_ruedita/2))
        )
rue2 = (cq.Workplane()
        .cylinder(alto_ruedita,radio_ruedita)
        .translate((-ancho_base_cajon/2 + margen_rueditas,-prof_base_cajon/2+margen_rueditas, alto_ruedita/2))
        )
rue3 = (cq.Workplane()
        .cylinder(alto_ruedita,radio_ruedita)
        .translate(( ancho_base_cajon/2 - margen_rueditas, prof_base_cajon/2-margen_rueditas, alto_ruedita/2))
        )
rue4 = (cq.Workplane()
        .cylinder(alto_ruedita,radio_ruedita)
        .translate(( ancho_base_cajon/2 - margen_rueditas,-prof_base_cajon/2+margen_rueditas, alto_ruedita/2)))

lado_cajon_izq = (cq.Workplane()
              .box(grosor_finger,prof_base_cajon,alto_cajon)
              .translate(((-ancho_base_cajon-grosor_finger)/2,0,alto_cajon/2+alto_ruedita))
              )
lado_cajon_der = (cq.Workplane()
              .box(grosor_finger,prof_base_cajon,alto_cajon)
              .translate((( ancho_base_cajon+grosor_finger)/2,0,alto_cajon/2+alto_ruedita))
              )

base_cajon = (cq.Workplane()
              .box(ancho_base_cajon,prof_base_cajon,grosor_lamina)
              .translate((0,0,grosor_soporte + alto_ruedita+grosor_lamina/2))
              )

fondo_cajon = (cq.Workplane()
              .box(ancho_base_cajon+2*grosor_finger,grosor_finger,alto_cajon)
              .translate((0,prof_base_cajon/2+grosor_finger/2,alto_cajon/2+alto_ruedita))
              )
frente_cajon = (cq.Workplane()
              .box(ancho_tapa_cajon,grosor_finger,alto_frente-alto_ruedita)
              .translate((ancho_pata/4,-prof_base_cajon/2-grosor_finger/2,alto_frente/2+alto_ruedita/2))
              )

soporte_cajon_fre = (
    cq.Workplane()
    .box(ancho_base_cajon,ancho_cajon_soporte,grosor_soporte)
    .translate((0,-prof_base_cajon/2+ancho_cajon_soporte/2,alto_ruedita+grosor_soporte/2))
    )

soporte_cajon_fon = (
    cq.Workplane()
    .box(ancho_base_cajon,ancho_cajon_soporte,grosor_soporte)
    .translate((0, prof_base_cajon/2-ancho_cajon_soporte/2,alto_ruedita+grosor_soporte/2))
    )

soporte_cajon_izq = (
    cq.Workplane()
    .box(ancho_cajon_soporte,prof_base_cajon-2*ancho_cajon_soporte,grosor_soporte)
    .translate((ancho_base_cajon/2-ancho_cajon_soporte/2,0,alto_ruedita+grosor_soporte/2))
    )

soporte_cajon_med = (
    cq.Workplane()
    .box(ancho_cajon_soporte,prof_base_cajon-2*ancho_cajon_soporte,grosor_soporte)
    .translate((0,0,alto_ruedita+grosor_soporte/2))
    )

soporte_cajon_der = (
    cq.Workplane()
    .box(ancho_cajon_soporte,prof_base_cajon-2*ancho_cajon_soporte,grosor_soporte)
    .translate((-ancho_base_cajon/2+ancho_cajon_soporte/2,0,alto_ruedita+grosor_soporte/2))
    )


cajon1 =  (cq.Workplane()
         .union(rue1)
         .union(rue2)
         .union(rue3)
         .union(rue4)
         .union(soporte_cajon_fon)
         .union(soporte_cajon_fre)
         .union(soporte_cajon_der)
         .union(soporte_cajon_med)
         .union(soporte_cajon_izq)
         .union(base_cajon)
         .union(lado_cajon_izq)
         .union(lado_cajon_der)
         .union(fondo_cajon)
         .union(frente_cajon)
        )

cajon1 = cajon1.translate((ancho_agujero_cajon/2+ancho_pata/2,-prof_agujero_cajon/2-grosor_finger/2,0))
cajon2 = cajon1.mirror(mirrorPlane="YZ")
cajon3 = cajon1.mirror(mirrorPlane="YZ").mirror(mirrorPlane=("XZ"))
cajon4 = cajon1.mirror(mirrorPlane="XZ").translate((0,200,0))

frente_cama = (
    cq.Workplane()
    .box(grosor_finger,ancho_cama,alto_frente)
    .translate((largo_cama/2-grosor_finger/2,0,alto_frente/2))
    )

respaldo_cama = (
    cq.Workplane()
    .box(grosor_finger,ancho_cama,alto_respaldo)
    .translate((-largo_cama/2+grosor_finger/2,0,alto_respaldo/2))
    )

# 
# marco de la parrilla
# 
marco_parrilla_lat = (
    cq.Workplane()
    .box(largo_parrilla,grosor_parrilla,alto_soporte_parrilla)
    .translate((0,0,alto_soporte_parrilla/2))
    )

marco_parrilla_fre = (
    cq.Workplane()
    .box(grosor_parrilla,ancho_parrilla,alto_soporte_parrilla)
    .translate((largo_cama/2-grosor_finger-grosor_parrilla/2,0,alto_soporte_parrilla/2 + alto_cajon+alto_ruedita))
    )

marco_parrilla_res = marco_parrilla_fre.mirror(mirrorPlane="YZ")
marco_parrilla_cen = marco_parrilla_lat.translate((0,0,cota_marco))
marco_parrilla_izq = marco_parrilla_lat.translate((0,-ancho_cama/2+grosor_parrilla/2+grosor_finger,cota_marco))
marco_parrilla_der = marco_parrilla_izq.mirror(mirrorPlane="XZ")

#
# tablas de la parrilla
#
tabla_x0 = -largo_cama/2+grosor_finger+ancho_tabla/2
tabla_x1 = -tabla_x0
dx = (tabla_x1-tabla_x0)/6
tabla_parrilla = (cq.Workplane()
                  .box(ancho_tabla, ancho_parrilla, grosor_tabla)
                  .translate((0,0,cota_tabla))
                 )
parrilla = (cq.Workplane()
            .union(marco_parrilla_res)
            .union(marco_parrilla_fre)
            .union(marco_parrilla_izq)
            .union(marco_parrilla_cen)
            .union(marco_parrilla_der)
            )

x = tabla_x0
while x <= tabla_x1:
    parrilla = parrilla.union(tabla_parrilla.translate((x,0,0)))
    x += dx

#
# patas
#
pata_cen_cen = (cq.Workplane()
            .box(ancho_pata,ancho_pata,cota_marco)
            .translate((0,0,cota_marco/2))
            )
pata_cen_der = pata_cen_cen.translate((0,ancho_parrilla/2-ancho_pata/2,0))
pata_cen_izq = pata_cen_cen.translate((0,-ancho_parrilla/2+ancho_pata/2,0))

pata_fre_cen = pata_cen_cen.translate((largo_parrilla/2,0,0))
pata_fre_der = pata_fre_cen.translate((0,ancho_parrilla/2-ancho_pata/2,0))
pata_fre_izq = pata_fre_cen.translate((0,-ancho_parrilla/2+ancho_pata/2,0))

pata_res_cen = pata_cen_cen.translate((-largo_parrilla/2,0,0))
pata_res_der = pata_res_cen.translate((0,ancho_parrilla/2-ancho_pata/2,0))
pata_res_izq = pata_res_cen.translate((0,-ancho_parrilla/2+ancho_pata/2,0))

patas = (cq.Workplane()
         .union(pata_cen_cen)
         .union(pata_cen_der)
         .union(pata_cen_izq)
         .union(pata_fre_cen)
         .union(pata_fre_der)
         .union(pata_fre_izq)
         .union(pata_res_cen)
         .union(pata_res_der)
         .union(pata_res_izq)
         )
#
# colchon, para referencia
#
colchon = (
    cq.Workplane()
    .box(largo_colchon,ancho_colchon,alto_colchon)
    .fillet(50)
    .translate((0,0,alto_colchon/2+base_colchon))
)

#
# rendering con colores y eso
#    
color_cajon = cq.Color(0.7,0.6,0.4)
color_colchon = cq.Color(0.5,0.6,0.9,0.5)


res = (cq.Assembly()
.add(colchon,color=color_colchon)
.add(cajon1,color=color_cajon)
.add(cajon2,color=color_cajon)
.add(cajon3,color=color_cajon)
.add(cajon4,color=color_cajon)
.add(frente_cama)
.add(respaldo_cama)
.add(parrilla,color=cq.Color("yellow"))
.add(patas,color=cq.Color("orange"))
)

vis.show(res)
#show_object(res,name="www")


