import os
import base64
import datetime
import string
from bottle import route, default_app, template, run, static_file, error, post, get, redirect, view, request, response, HTTPResponse, debug
from lxml import etree
from pymongo import MongoClient as Connection
from pymongo import DESCENDING
import StringIO
#import pandas as pd
import numpy as np
import shapefile
#import matplotlib.pyplot as plt
import gridfs
import urllib


import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def dibujaMunicipiosErrores(first,micolor,finrango1, finrango2, fin, ax):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.path import Path
    import matplotlib.patches as patches
    dibuja= True
    if micolor==0:
        micolor2='green'
    elif (micolor==1): 
        micolor2='yellow'
    else:
        micolor2='red'

    for i in range(1,4):
        if (i==1):
            dibuja= True
            initrango=0
            finrango=finrango1
        if (i==2):
            if(finrango1==finrango2):
             dibuja=False
            else:    
             dibuja= True
             initrango=finrango1+1
             finrango=finrango2
        if (i==3):
            dibuja= True
            initrango=finrango2+1
            finrango=fin   
            
        if (dibuja==True):    
         x= [i[0] for i in first.shape.points[initrango:finrango]]
         y= [i[1] for i in first.shape.points[initrango:finrango]]
         npx = np.array(x)
         npy = np.array(y)
         npxy = np.vstack((npx,npy)).T
         verts = npxy

         l = [Path.LINETO] * len(first.shape.points[initrango:finrango])
         l[0]=Path.MOVETO
         l[-1]=Path.CLOSEPOLY
         codes = l
         path = Path(verts, codes, closed=False)
         patch = patches.PathPatch(path, facecolor=micolor2, lw=1)
         ax.add_patch(patch)

def dibujaMunicipios(first,micolor, ax):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.path import Path
    import matplotlib.patches as patches
    if micolor==0:
        micolor2='green'
    elif (micolor==1): 
        micolor2='yellow'
    else:
        micolor2='red'
    x= [i[0] for i in first.shape.points[:]]
    y= [i[1] for i in first.shape.points[:]]
    npx = np.array(x)
    npy = np.array(y)
    npxy = np.vstack((npx,npy)).T
    verts = npxy

    l = [Path.LINETO] * len(first.shape.points[:])
    l[0]=Path.MOVETO
    l[-1]=Path.CLOSEPOLY
    codes = l
    path = Path(verts, codes, closed=False)
    patch = patches.PathPatch(path, facecolor=micolor2, lw=1)
    ax.add_patch(patch)
	
   
def nuevoReporte(municipio, nivel_alerta):
    #Conectamos a la base de datos
    import base64
    import json
    from pymongo import MongoClient as Connection

    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1
    #db = Connection().othesoluciones1
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
	from pymongo import MongoClient as Connection
	cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
	MONGODB_URI =cadenaCon
	conexion = Connection(MONGODB_URI)
	db = conexion.othesoluciones1
	import gridfs
    #fs = gridfs.GridFS(db,"fs").get_version(["ALERTAS.png"])	
    #plot_url_img   = base64.b64encode(fs.read())
	fs = gridfs.GridFS(db)
	#print list(db.fs.files.find())
	gridout = fs.get_last_version("ALERTAS.png")
	plot_url_img = base64.b64encode(gridout.read())
	''' List noticias. '''
	PAGE_SIZE = 10
	noticias_del_dia = (db.noticias_del_dia.find().sort('Fecha de busqueda', DESCENDING).limit(PAGE_SIZE))
	print noticias_del_dia
	return {'noticias_del_dia': noticias_del_dia, 'plot_url_img':plot_url_img }		
	

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
    #db = Connection().othesoluciones1
    collection1 = db.prediccionesAEMET 
    print elimina_tildes(name.decode('utf-8'))
    name2 =  elimina_tildes(name.decode('utf-8'))
    cursor1 = collection1.find_one({"Municipio": name2})
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
    varmun = str(reporte['municipio'])
    print type(varmun), "<---", type(reporte['municipio'])
    varniv = int(reporte['nivel_de_alerta'])
    print type(varniv), "<---", type(reporte['nivel_de_alerta'])
    #nuevoReporte(reporte['municipio'],reporte['nivel_de_alerta'])
    nuevoReporte(varmun,varniv)
    return template("p_reporte.tpl", muni=muni, nivel=nivel,alta=alta)	
    #redirect('/reporte')
 else:
    listaErrores=[]
    if (reporte['municipio']=='ninguno'):
       municipio_OK=False
    else:
	   municipio_OK=True
    listaErrores.append(municipio_OK)
    if (reporte['nivel_de_alerta']=='ninguno'):
	    alerta_OK=False
    else:
		alerta_OK=True
    listaErrores.append(alerta_OK)
      #return template("error_views/p_reporte_error_municipio.tpl", muni=muni, nivel=nivel, nivsel=reporte['nivel_de_alerta'])
    return template("error_views/p_reporte_error.tpl", muni=muni, nivel=nivel, nivsel=reporte['nivel_de_alerta'], munsel=reporte['municipio'], errores=listaErrores)
#    else: 
#      print reporte['municipio']
#      return template("error_views/p_reporte_error_nivel_alerta.tpl", muni=muni, nivel=nivel, munsel=reporte['municipio'])





	
#@route('/predicciones')
#def predicciones():
	#doc=etree.parse("sevilla.xml")
	#muni=doc.findall("municipio")
	#return template("p_predicciones.tpl", mun=muni)
	#img = StringIO.StringIO()
	#sf = shapefile.Reader("static/Municipios/200001493.shp")
	#plt.figure(figsize=(5,5))
	#for shape in sf.shapeRecords():
	#	x= [i[0] for i in shape.shape.points[:]]
	#	y= [i[1] for i in shape.shape.points[:]]
	#	plt.plot(x,y)
	#plt.axis('off')	
	#plt.savefig(img, format='png')
	#img.seek(0)
	#plot_url = base64.b64encode(img.getvalue())
#	return template("p_predicciones.tpl")#, plot_url=plot_url)

@route('/predicciones')
def predicciones():
    from time import time
    tiempo_inicial=time()
    import shapefile
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    import matplotlib.patches as patches
    import base64
    import datetime
    from pymongo import MongoClient as Connection
    ##Conexion a MongoDB
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon 
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1
    #########################
    #Diccionario creado a mano para dibujar de forma distinta los municipios
    # que tienen terrenos que no estan unidos entre si
    diccionarioMunicipiosErroneos = {}
    diccionarioMunicipiosErroneos['Mostoles']={'finrango1':1532 , 'finrango2':1532}
    diccionarioMunicipiosErroneos['Becerril de la Sierra']= {'finrango1':307 , 'finrango2':408}
    diccionarioMunicipiosErroneos['Boalo, El']= {'finrango1':342 , 'finrango2':756 }
    diccionarioMunicipiosErroneos['Manzanares El Real']= {'finrango1':705 , 'finrango2':819 }
    diccionarioMunicipiosErroneos['Moralzarzal']= {'finrango1':558 , 'finrango2':558 }
    diccionarioMunicipiosErroneos['Mostoles']= {'finrango1':1532 , 'finrango2':1532 }
    diccionarioMunicipiosErroneos['Navacerrada']= {'finrango1':446 , 'finrango2':446 }
    diccionarioMunicipiosErroneos['Santa Maria de la Alameda']= {'finrango1':6740 , 'finrango2':6740 }
    diccionarioMunicipiosErroneos['Serranillos del Valle']= {'finrango1':931 , 'finrango2':931 }
    diccionarioMunicipiosErroneos['Valdepielagos']= {'finrango1':909 , 'finrango2':909 }

    #########################
    #Dibujamos el mapa de Madrid en 3 colores en funcion del nivel de alerta en el que se encuentre cada municipio
    from lxml import etree
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    sf = shapefile.Reader("static/Municipios/200001493.shp")
    shapes =sf.shapeRecords()

    img = StringIO.StringIO()
    fig = plt.figure(figsize=(11,11))
    ax = fig.add_subplot(111)
    
    hoy = (datetime.date.today()+datetime.timedelta(days=0)).strftime('%d-%m-%Y')


    for shape in sf.shapeRecords():
        nombreMunicipio = elimina_tildes((shape.record[2]).decode('windows-1252'))
        name2=nombreMunicipio
        if(name2=="Manzanares El Real"):
            name2="Manzanares el Real"
        collection1=db.PrediccionOTHE
        cursor1=collection1.find_one({"Municipio": name2})
        predHoy = cursor1["Nivel "+hoy]
        color=int(predHoy)
        if (nombreMunicipio in diccionarioMunicipiosErroneos):
            finrango1= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango1']
            finrango2= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango2']
            dibujaMunicipiosErrores(shape,int(color),finrango1,finrango2,len(shape.shape.points), ax)
        else:
            dibujaMunicipios(shape,int(color), ax)



    ax.autoscale_view()


    plt.axis('off')
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue())
    conexion.close()
    tiempo_final = time() 
 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
 
    print 'El tiempo de ejecucion fue:',tiempo_ejecucion #En segundos
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
    manana = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%d/%m/%Y')
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    alta=0
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
            'next_page': next_page, 'alta':alta, 'muni':muni, 'fdesde':manana, 'fhasta':manana
            }	

# para PRO hay que ponerle 2 horas +
@post('/notifica')
def notifica(page=0):
 manana = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%d/%m/%Y')
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
 print request.POST['fechaHasta']
 fechaHastaIns= datetime.datetime.strptime(request.POST['fechaHasta'],'%d/%m/%Y')
 fechaDesdeIns= datetime.datetime.strptime(request.POST['fechaDesde'],'%d/%m/%Y')
 notif = {'email': request.POST['email'], 'fdesde':request.POST['fechaDesde'], 'fhasta':request.POST['fechaHasta'],
               'municipio': request.POST['municipio'],
               'realizada': datetime.datetime.now()}
 #notif = {'email': request.POST['email'], 'fdesde':fechaDesdeIns, 'fhasta':fechaHastaIns,
 #              'municipio': request.POST['municipio'],
 #              'realizada': datetime.datetime.now()}			   
 listaErrores=[]			   
 #Chequeamos el email
 import re
 email_address = request.POST['email']
 #Step 1: Check email
 #Check using Regex that an email meets minimum requirements, throw an error if not
 addressToVerify = email_address
 match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
 
 if match == None:
    #print('Bad Syntax in ' + addressToVerify)
    mail_OK=False
    mailSel=""
 else:
    mail_OK=True
    mailSel=email_address
 print mail_OK
 listaErrores.append(mail_OK)	
 #Chequeamos el municipio	
 doc=etree.parse("static/Municipios/madrid.xml")
 muni=doc.findall("municipio")
 if (notif['municipio']=='ninguno'):
  municipio_OK=False
 else:
  municipio_OK=True
 listaErrores.append(municipio_OK)
 
 if ((notif['fdesde']=='')or(notif['fdesde']=='')):
  fechas_OK=False
 else:
  fechas_OK=True
  
 listaErrores.append(fechas_OK) 
 cuentaErrores= listaErrores.count(False)
 print cuentaErrores
 if(cuentaErrores==0):
     alta=1
     db.coleccion_notificaciones.insert(notif)
     return template("p_notificaciones.tpl", muni=muni, alta=alta, coleccion_notificaciones=coleccion_notificaciones, prev_page=prev_page, next_page=next_page, fdesde=manana, fhasta=manana )	
 else:
  return template("error_views/p_notificaciones_error.tpl", muni=muni, errores=listaErrores, coleccion_notificaciones=coleccion_notificaciones, prev_page=prev_page, next_page=next_page, munsel=notif['municipio'], mailSel=mailSel, fdesde=notif['fdesde'], fhasta=notif['fhasta'] )			
    
 #db.coleccion_notificaciones.insert(notif)
 #redirect('/notificaciones')



	 
cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
MONGODB_URI =cadenaCon
MONGODB_URI = 'mongodb://othesoluciones:othesoluciones@ds029635.mlab.com:29635/othesoluciones1'


db = Connection(MONGODB_URI).othesoluciones1

#Para ejecutar con BBDD local 
#db = Connection().othesoluciones1


run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
