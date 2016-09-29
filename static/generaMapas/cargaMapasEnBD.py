def inserta_y_borra():
	import shapefile
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib.path import Path
	import matplotlib.patches as patches
	import os
	import unicodedata
	def elimina_tildes(s):
	   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
	 
	#Conectamos a la base de datos
	import base64
	import json
	from pymongo import MongoClient as Connection
	from bs4 import BeautifulSoup

	cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
	MONGODB_URI =cadenaCon
	conexion = Connection(MONGODB_URI)
	db = conexion.othesoluciones1
	import gridfs
	imagesfs = gridfs.GridFS(db,'images')

	sf = shapefile.Reader("../Municipios/200001493.shp")
	for shape in sf.shapeRecords():
		nombreMunicipio = elimina_tildes((shape.record[2]).decode('windows-1252'))
		#pagina hoy_mun azul
		img_municipio="./dirTempGeneraMapas/"+nombreMunicipio+"-BLUE.png"
		img_municipio_cam="./dirTempGeneraMapas/"+nombreMunicipio+"-CAM-BLUE.png"
		file_img_municipio=file(img_municipio,'rb')
		file_img_municipio_cam=file(img_municipio_cam,'rb')
		filename_img_municipio=nombreMunicipio+"-BLUE.png"
		filename_img_municipio_cam=nombreMunicipio+"-CAM-BLUE.png"

		#predicciones baja
		img_municipio_bajo="./dirTempGeneraMapas/"+nombreMunicipio+"-Bajo.png"
		img_municipio_cam_bajo="./dirTempGeneraMapas/"+nombreMunicipio+"-CAM-Bajo.png"
		file_img_municipio_bajo=file(img_municipio_bajo,'rb')
		file_img_municipio_cam_bajo=file(img_municipio_cam_bajo,'rb')
		filename_img_municipio_bajo=nombreMunicipio+"-Bajo.png"
		filename_img_municipio_cam_bajo=nombreMunicipio+"-CAM-Bajo.png"    

		#predicciones medio
		img_municipio_medio="./dirTempGeneraMapas/"+nombreMunicipio+"-Medio.png"
		img_municipio_cam_medio="./dirTempGeneraMapas/"+nombreMunicipio+"-CAM-Medio.png"
		file_img_municipio_medio=file(img_municipio_medio,'rb')
		file_img_municipio_cam_medio=file(img_municipio_cam_medio,'rb')
		filename_img_municipio_medio=nombreMunicipio+"-Medio.png"
		filename_img_municipio_cam_medio=nombreMunicipio+"-CAM-Medio.png"  
		
		#predicciones alto
		img_municipio_alto="./dirTempGeneraMapas/"+nombreMunicipio+"-Alto.png"
		img_municipio_cam_alto="./dirTempGeneraMapas/"+nombreMunicipio+"-CAM-Alto.png"
		file_img_municipio_alto=file(img_municipio_alto,'rb')
		file_img_municipio_cam_alto=file(img_municipio_cam_alto,'rb')
		filename_img_municipio_alto=nombreMunicipio+"-Alto.png"
		filename_img_municipio_cam_alto=nombreMunicipio+"-CAM-Alto.png"  
		
		imagenes = {
			"municipio": nombreMunicipio,
			"filename_img_municipio": filename_img_municipio,
			"filename_img_municipio_cam": filename_img_municipio_cam,
			
			"filename_img_municipio_bajo": filename_img_municipio_bajo,
			"filename_img_municipio_cam_bajo": filename_img_municipio_cam_bajo,
			
			"filename_img_municipio_medio": filename_img_municipio_medio,
			"filename_img_municipio_cam_medio": filename_img_municipio_cam_medio,
			
			"filename_img_municipio_alto": filename_img_municipio_alto,
			"filename_img_municipio_cam_alto": filename_img_municipio_cam_alto
			
		}
		imagesfs.put(file_img_municipio, filename=filename_img_municipio)
		imagesfs.put(file_img_municipio_cam, filename=filename_img_municipio_cam)
		
		imagesfs.put(file_img_municipio_bajo, filename=filename_img_municipio_bajo)
		imagesfs.put(file_img_municipio_cam_bajo, filename=filename_img_municipio_cam_bajo)
		
		imagesfs.put(file_img_municipio_medio, filename=filename_img_municipio_medio)
		imagesfs.put(file_img_municipio_cam_medio, filename=filename_img_municipio_cam_medio)
		
		imagesfs.put(file_img_municipio_alto, filename=filename_img_municipio_alto)
		imagesfs.put(file_img_municipio_cam_alto, filename=filename_img_municipio_cam_alto)
		

		db.imagenes.insert(imagenes)
		
		file_img_municipio.close()
		os.remove(img_municipio)
		
		file_img_municipio_cam.close()
		os.remove(img_municipio_cam)
		
		file_img_municipio_bajo.close()
		os.remove(img_municipio_bajo)
		
		file_img_municipio_cam_bajo.close()
		os.remove(img_municipio_cam_bajo)
		
		file_img_municipio_medio.close()
		os.remove(img_municipio_medio)
		
		file_img_municipio_cam_medio.close()
		os.remove(img_municipio_cam_medio)
		
		file_img_municipio_alto.close()
		os.remove(img_municipio_alto)
		
		file_img_municipio_cam_alto.close()
		os.remove(img_municipio_cam_alto)
		print "Insertado y Borrado:", nombreMunicipio

	imagesfs = gridfs.GridFS(db,'color-zona')

	#Insertamos la imagen del mapa completo
	img_municipios="dirTempGeneraMapas/COLOR.png"
	file_img_municipios=file(img_municipios,'rb')
	filename_img_municipios="COLOR.png"
	imagesfs.put(file_img_municipios, filename=filename_img_municipios)
	file_img_municipios.close()
	os.remove(img_municipios)
	print "Insertado y borrado: ", img_municipios
	#Insertamos la imagen de la leyenda
	img_leyenda="dirTempGeneraMapas/Leyenda.png"
	file_img_leyenda=file(img_leyenda,'rb')
	filename_img_leyenda="Leyenda.png"
	imagesfs.put(file_img_leyenda, filename=filename_img_leyenda)

	file_img_leyenda.close()
	os.remove(img_leyenda)
	print "Insertado y borrado: ", img_leyenda
	os.rmdir("dirTempGeneraMapas")