import os
import datetime
import string
from bottle import route, default_app, template, run, static_file, error, post, get, redirect, view, request
from lxml import etree
from pymongo import MongoClient as Connection
from pymongo import DESCENDING

@route('/')
def index():
    doc=etree.parse("sevilla.xml")
    muni=doc.findall("municipio")
    return template("index.tpl", mun=muni)
	
@route('/hoy')
def hoy():
	doc=etree.parse("sevilla.xml")
	muni=doc.findall("municipio")
	return template("p_hoy.tpl", mun=muni)
	
@route('/reporte')
def reporte():
	return template("p_reporte.tpl")
	

	
@route('/predicciones')
def predicciones():
	doc=etree.parse("sevilla.xml")
	muni=doc.findall("municipio")
	return template("p_predicciones.tpl", mun=muni)

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
                .sort('date', DESCENDING)
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE))
    return {'coleccion_notificaciones': coleccion_notificaciones,
            'prev_page': prev_page,
            'next_page': next_page,
            }	
	
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

db = Connection(MONGODB_URI).othesoluciones1

#Para ejecutar con BBDD local 
#db = Connection().othesoluciones1

run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))