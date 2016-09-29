import os

if not os.path.exists("dirTempGeneraMapas"):
    print "Lo creo"
    os.makedirs("dirTempGeneraMapas")
	
from mapasALTOS_Funciones import dibujaMapasNivelAlto
dibujaMapasNivelAlto()

from mapasAZULES_Funciones import dibujaMapasAzules
dibujaMapasAzules()

from mapasBAJOS_Funciones import dibujaMapasNivelBajo
dibujaMapasNivelBajo()

from mapasMEDIOS_Funciones import dibujaMapasNivelMedio
dibujaMapasNivelMedio()

from mapaZonal import dibuja_mapa_zonal, dibujaLeyenda
dibuja_mapa_zonal()
dibujaLeyenda()

from cargaMapasEnBD import inserta_y_borra
inserta_y_borra()
