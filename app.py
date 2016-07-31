import os
from bottle import route, default_app, template, run, static_file, error
from lxml import etree
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
	
@route('/notificaciones')
def notificaciones():
	return template("p_notificaciones.tpl")
	
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

run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))