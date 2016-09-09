import os
import base64
import datetime
import string
from bottle import route, default_app, template, run, static_file, error, post, get, redirect, view, request, response, HTTPResponse, debug
from lxml import etree
from pymongo import MongoClient as Connection
from pymongo import DESCENDING
import StringIO
import pandas as pd
import numpy as np
import shapefile
import matplotlib.pyplot as plt
import gridfs
import urllib



import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def nuevoReporte(municipio, nivel_alerta):
    #Conectamos a la base de datos
    import base64
    import json
    from pymongo import MongoClient as Connection

    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1
    
    hoy = datetime.date.today().strftime('%d-%m-%Y')
  
    nivelViejo = db.PrediccionOTHE.find_one({"Codigo": municipio})['Nivel '+str(hoy)] 
    nuevoNivel = nivelViejo+(nivel_alerta-nivelViejo)*0.25

    db.PrediccionOTHE.update_one({"Codigo": municipio},{'$set':{'Nivel '+str(hoy):nuevoNivel}}, upsert=False)
    conexion.close()
	
#@route('/')
@get(['/'])
@view('index')
def index():
    #doc=etree.parse("sevilla.xml")
    #muni=doc.findall("municipio")
    #return template("index.tpl", mun=muni)
	''' List noticias. '''
	PAGE_SIZE = 10
	noticias_del_dia = (db.noticias_del_dia.find().sort('Fecha de busqueda', DESCENDING).limit(PAGE_SIZE))
	print noticias_del_dia
	return {'noticias_del_dia': noticias_del_dia }	
	

@get(['/hoy', '/hoy/:page#\d+#'])
@view('p_hoy')
def hoy(page=0):
    ''' List messages. '''
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    PAGE_SIZE = 3
    page = int(page)
    prev_page = None
    if page > 0:
        prev_page = page - 1
    next_page = None
    if db.calidad_aire.count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    calidad_aire = (db.calidad_aire.find()
                .sort('Estacion')
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE))
    return {'calidad_aire': calidad_aire,
            'prev_page': prev_page,
            'next_page': next_page,
            'muni': muni
            }	


#@route('/<cod>/<name>')
@get(['/<cod>/<name>'])
@view('p_hoy_mun')
def hoy_mun(cod,name):
    import datetime
    import time
    import base64
    import json
    from pymongo import MongoClient as Connection
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1
    collection1 = db.prediccionesAEMET 
    #name2=elimina_tildes(unicode(name))
    print name, "€€->"#,name2
    cursor1 = collection1.find_one({"Municipio": name})
    busquedaAEMET = cursor1[time.strftime("%Y-%m-%d")]
    #img = StringIO.StringIO()
    #sf = shapefile.Reader("static/Municipios/200001493.shp")
    #geomet = sf.shapeRecords()
    #plt.figure(figsize=(2,2))
    #i = 0
    #while ((elimina_tildes((sf.record(i)[2]).decode('windows-1252'))!=elimina_tildes(name.decode('utf-8'))) and (i<len(list(sf.iterRecords())))): i=i+1
    #first = geomet[i]
    #x= [i[0] for i in first.shape.points[:]]
    #y= [i[1] for i in first.shape.points[:]]
    #plt.plot(x,y)
    #plt.axis('off')	
    #plt.savefig(img, format='png')
    #img.seek(0)
    #plot_url = base64.b64encode(img.getvalue())
    collection2 = db.imagenes
    cursor2 = collection2.find_one({'municipio':name2})
    print cursor2['filename_img_municipio']
    print cursor2['filename_img_municipio_cam']
    #f1 = gridfs.GridFS(db,"images").get_version("Ajalvir.png")
    f1 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio'])
    plot_url_img = base64.b64encode(f1.read())
    #f2 = gridfs.GridFS(db,"images").get_version("Ajalvir.png")
    f2 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio_cam'])
    plot_url_img_cam = base64.b64encode(f2.read())
    #return template("p_hoy_mun.tpl",name=name,plot_url=plot_url, busquedaAEMET=busquedaAEMET,plot_url_img=plot_url_img, plot_url_img_cam=plot_url_img_cam)
    return template("p_hoy_mun.tpl",name=name, busquedaAEMET=busquedaAEMET,plot_url_img=plot_url_img, plot_url_img_cam=plot_url_img_cam)

	
#@route('/reporte')
#def reporte():
	#return template("p_reporte.tpl")
@route('/reporte')
def reporte():
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    doc=etree.parse("static/Municipios/niveles.xml")
    nivel=doc.findall("nivel")
    alta = 0
    return template("p_reporte.tpl", muni=muni, nivel=nivel,alta=alta)	


@post('/reporta')
def notifica():
 doc=etree.parse("static/Municipios/madrid.xml")
 muni=doc.findall("municipio")
 doc=etree.parse("static/Municipios/niveles.xml")
 nivel=doc.findall("nivel")
 reporte = {'municipio': request.POST['municipio'],
               'nivel_de_alerta': request.POST['nivel_de_alerta'],
               'realizada': datetime.datetime.now()}	
 print "municipio",  reporte['municipio']
 if ((reporte['municipio']!='ninguno') and (reporte['nivel_de_alerta']!='ninguno')):	
    db.coleccion_reportes.insert(reporte)
    alta = 1
    nuevoReporte(muni,nivel)
    return template("p_reporte.tpl", muni=muni, nivel=nivel,alta=alta)	
    #redirect('/reporte')
 else:
    if (reporte['municipio']=='ninguno'):
      return template("error_views/p_reporte_error_municipio.tpl", muni=muni, nivel=nivel, nivsel=reporte['nivel_de_alerta'])
    else: 
      print reporte['municipio']
      return template("error_views/p_reporte_error_nivel_alerta.tpl", muni=muni, nivel=nivel, munsel=reporte['municipio'])





	
@route('/predicciones')
def predicciones():
	#doc=etree.parse("sevilla.xml")
	#muni=doc.findall("municipio")
	#return template("p_predicciones.tpl", mun=muni)
	img = StringIO.StringIO()
	sf = shapefile.Reader("static/Municipios/200001493.shp")
	plt.figure(figsize=(5,5))
	for shape in sf.shapeRecords():
		x= [i[0] for i in shape.shape.points[:]]
		y= [i[1] for i in shape.shape.points[:]]
		plt.plot(x,y)
	plt.axis('off')	
	plt.savefig(img, format='png')
	img.seek(0)
	plot_url = base64.b64encode(img.getvalue())
	return template("p_predicciones.tpl", plot_url=plot_url)
	
	
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')
	
@error(404)
def error404(error):
    return 'Nothing here, sorry'


@get(['/notificaciones', '/notificaciones/:page#\d+#'])
@view('p_notificaciones')
def notificaciones(page=0):
    ''' List messages. '''
    PAGE_SIZE = 5
    page = int(page)
    prev_page = None
    if page > 0:
        prev_page = page - 1
    next_page = None
    if db.coleccion_notificaciones.count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    coleccion_notificaciones = (db.coleccion_notificaciones.find()
                .sort('realizada', DESCENDING)
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE))
    return {'coleccion_notificaciones': coleccion_notificaciones,
            'prev_page': prev_page,
            'next_page': next_page,
            }	

# para PRO hay que ponerle 2 horas +
@post('/notifica')
def notifica():
 notif = {'email': request.POST['email'],
               'captador': request.POST['captador'],
               'periodicidad': request.POST['periodicidad'],
               'realizada': datetime.datetime.now()}
 db.coleccion_notificaciones.insert(notif)
 redirect('/notificaciones')



	 
cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
MONGODB_URI =cadenaCon
#MONGODB_URI = 'mongodb://othesoluciones:othesoluciones@ds029635.mlab.com:29635/othesoluciones1'


db = Connection(MONGODB_URI).othesoluciones1

#Para ejecutar con BBDD local 
#db = Connection().othesoluciones1


run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
