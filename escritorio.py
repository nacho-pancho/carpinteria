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
# escritorio de esquina de 2 piezas
#
grosor_finger      = 20
alto_ppal = 750
prof_ppal = 600
ancho_ppal = 1500
alto_sec = 650
prof_sec = 500
ancho_sec = 1500
alto_fondo = 300
prof_bandeja = 100
tabla_ppal = (cq.Workplane()
               .box(ancho_ppal,prof_ppal,grosor_finger)
               .translate((0,0,alto_ppal-grosor_finger/2))
               )
pata_ppal_der = (cq.Workplane()
                 .box(grosor_finger,prof_ppal,alto_ppal-grosor_finger)
                 .translate(((ancho_ppal-grosor_finger)/2,0,(alto_ppal-grosor_finger)/2))
                 )
pata_ppal_izq = (cq.Workplane()
                 .box(grosor_finger,prof_ppal,alto_ppal-grosor_finger)
                 .translate((-(ancho_ppal-grosor_finger)/2,0,(alto_ppal-grosor_finger)/2))
                 )
fondo_ppal = (cq.Workplane()
              .box(ancho_ppal,grosor_finger,alto_fondo)
              .translate((0,-prof_ppal/2+grosor_finger/2+prof_bandeja,alto_ppal-grosor_finger-alto_fondo/2))
              )
bandeja_ppal = (cq.Workplane()
               .box(ancho_ppal,prof_bandeja,grosor_finger)
               .translate((0,-prof_ppal/2+prof_bandeja/2,alto_ppal-alto_fondo-grosor_finger/2))
               )

tabla_sec = (cq.Workplane()
               .box(ancho_sec,prof_sec,grosor_finger)
               .translate((0,0,alto_sec-grosor_finger/2))
               )
pata_sec_der = (cq.Workplane()
                 .box(grosor_finger,prof_sec,alto_sec-grosor_finger)
                 .translate(((ancho_sec-grosor_finger)/2,0,(alto_sec-grosor_finger)/2))
                 )
pata_sec_izq = (cq.Workplane()
                 .box(grosor_finger,prof_sec,alto_sec-grosor_finger)
                 .translate((-(ancho_sec-grosor_finger)/2,0,(alto_sec-grosor_finger)/2))
                 )
fondo_sec = (cq.Workplane()
              .box(ancho_sec,grosor_finger,alto_fondo)
              .translate((0,-prof_sec/2+grosor_finger/2,alto_sec-grosor_finger-alto_fondo/2))
              )


pieza_ppal = tabla_ppal.union(pata_ppal_der).union(pata_ppal_izq).union(fondo_ppal).union(bandeja_ppal)
pieza_sec = tabla_sec.union(pata_sec_der).union(pata_sec_izq).union(fondo_sec).rotate(zero,zaxis,90).translate((prof_sec-grosor_finger,ancho_sec/2-prof_ppal/2+grosor_finger+prof_bandeja,0))
center = (cq.Workplane().sphere(50).translate((0,0,0)))

res = (cq.Assembly()
       .add(pieza_ppal,color=cq.Color(0.8,0.7,0.6),name="pieza_ppal")
       .add(pieza_sec,color=cq.Color(0.8,0.5,0.8),name="pieza_sec")
       .add(center,name="center")   
       )

vis.show(res)
#show_object(res,name="www")


