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

def conexion_bbdd():
    import base64
    from pymongo import MongoClient as Connection
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
	#para local return Connection()
    return Connection(MONGODB_URI)



import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def dibujaMunicipiosErrores(first,micolor,finrango1, finrango2, fin, ax):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.path import Path
    import matplotlib.patches as patches
    dibuja= True
    if ((0<=micolor) and (micolor<1)):
        micolor2='green'
    else:
    	if ((1<=micolor)and(micolor<2)): 
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
	
    if ((0<=micolor) and (micolor<1)):
        micolor2='green'
    else:
    	if ((1<=micolor)and(micolor<2)): 
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

def dibuja_mapa_alertas():
    import StringIO
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

        #import random
        #predHoy= random.randint(0,2)
        color=round(predHoy)
        if (nombreMunicipio in diccionarioMunicipiosErroneos):
            finrango1= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango1']
            finrango2= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango2']
            dibujaMunicipiosErrores(shape,int(color),finrango1,finrango2,len(shape.shape.points), ax)
        else:
            dibujaMunicipios(shape,int(color), ax)



    ax.autoscale_view()
	
    red_patch = patches.Patch(color='red', label='Alto')
    yel_patch = patches.Patch(color='yellow', label='Medio')
    gre_patch = patches.Patch(color='green', label='Bajo')
    plt.legend(handles=[red_patch,yel_patch, gre_patch], fontsize=29, loc='upper left')

    plt.axis('off')
    nomMapaAlerta="static/Municipios/ALERTAS.png"
    plt.savefig(nomMapaAlerta, bbox_inches='tight')
    
    tiempo_final = time() 
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    #Genero la tabla de gridfs para almacenar imagenes
    import gridfs
    fs = gridfs.GridFS(db)
    db.drop_collection('fs.chunks')
    db.drop_collection('fs.files')
    file_img_alerta=file(nomMapaAlerta,'rb')
    fs.put(file_img_alerta,filename="ALERTAS.png")
    print 'El tiempo de ejecucion fue:',tiempo_ejecucion #En segundos
    import os
    conexion.close()
    file_img_alerta.close()
    os.remove(nomMapaAlerta)	
   
def nuevoReporte(municipio, nivel_alerta):
    #Conectamos a la base de datos
    import base64
    import json
    from pymongo import MongoClient as Connection
    import datetime

    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1
    
    hoy = datetime.date.today().strftime('%d-%m-%Y')
  
    nivelViejo = db.PrediccionOTHE.find_one({"Codigo": municipio})['Nivel '+str(hoy)] 
    #Reporte de un nivel superior sube de nivel al segundo reporte.
    #Reporte de dos niveles superiores sube al nivel intermedio al primer reporte.
    
    #Para bajar de nivel, difiere si el nivel ha sido calculado por el sistema, funciona igual que para subir.
    #Si el nivel ha sido modificado mediante reportes, bajara mas rapido dependiendo de numero de reportes con el que hubiese sido calculado.
    nuevoNivel = nivelViejo+(nivel_alerta-round(nivelViejo))*0.45

    if round(nuevoNivel)<1:
        nuevaAlerta='Bajo'
    else:
        if round(nuevoNivel)<2:
            nuevaAlerta='Medio'
        else:
            nuevaAlerta='Alto'

    db.PrediccionOTHE.update_one({"Codigo": municipio},{'$set':{'Nivel '+str(hoy):nuevoNivel}}, upsert=False)
    db.PrediccionOTHE.update_one({"Codigo": municipio},{'$set':{'Alerta '+str(hoy):nuevaAlerta}}, upsert=False)	
    conexion.close()
    
    print "Dibujo mapa alertas AL REPORTAR"
    dibuja_mapa_alertas()
    print "Dibujo mapa alertas AL REPORTAR"

def cargaNoticias():
    #import base64
    #from pymongo import MongoClient as Connection
    #cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    #MONGODB_URI =cadenaCon
    #conexion = Connection(MONGODB_URI)
    conexion = conexion_bbdd()
    db = conexion.othesoluciones1
    ''' List noticias. '''
    PAGE_SIZE = 10
    noticias_del_dia = (db.noticias_del_dia.find().sort('Fecha de busqueda', DESCENDING).limit(PAGE_SIZE))
    conexion.close()
    return noticias_del_dia	
	
#@route('/')
@get(['/'])
@view('index')
def index():
	#from pymongo import MongoClient as Connection
	#cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
	#MONGODB_URI =cadenaCon
	#conexion = Connection(MONGODB_URI)
	conexion = conexion_bbdd()
	db = conexion.othesoluciones1
	import gridfs
	fs = gridfs.GridFS(db)
	gridout = fs.get_last_version("ALERTAS.png")
	plot_url_img = base64.b64encode(gridout.read())
	noticias_del_dia=cargaNoticias()
	conexion.close()
	return {'noticias_del_dia': noticias_del_dia, 'plot_url_img':plot_url_img }		
	

@get(['/hoy', '/hoy/:page#\d+#'])
@view('p_hoy')
def hoy(page=0):
    # CARGA DE NOTICIAS DEL DIA
    noticias_del_dia=cargaNoticias()

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
    return {'noticias_del_dia': noticias_del_dia, 'calidad_aire': calidad_aire,
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

    if (cod=='notificaciones')
      return notificaciones(name)
	#Busqueda de datos en coleccion: prediccionesAEMET
    collection1 = db.prediccionesAEMET 
    print elimina_tildes(name.decode('utf-8'))
    name2 =  elimina_tildes(name.decode('utf-8'))
    print name2
    print cod
    cursorHoyM1 = collection1.find_one({"Municipio": name2})
    print time.strftime("%Y-%m-%d")
    busquedaAEMET = cursorHoyM1[time.strftime("%Y-%m-%d")]
	#Carga de imagenes del municipio
    collection2 = db.imagenes
    cursorHoyM2 = collection2.find_one({'municipio':name2})
    print cursorHoyM2['filename_img_municipio']
    print cursorHoyM2['filename_img_municipio_cam']
    f1 = gridfs.GridFS(db,"images").get_version(cursorHoyM2['filename_img_municipio'])
    plot_url_img = base64.b64encode(f1.read())
    f2 = gridfs.GridFS(db,"images").get_version(cursorHoyM2['filename_img_municipio_cam'])
    plot_url_img_cam = base64.b64encode(f2.read())
	#Busqueda de datos en coleccion:calidad_aire_por_municipio 
    collection3= db.calidad_aire_por_municipio
    cursor3 = collection3.find_one({'Municipio':name2})
	#Carga de las noticias del dia
    noticias_del_dia=cargaNoticias()
    return template("p_hoy_mun.tpl",name=name, busquedaAEMET=busquedaAEMET,plot_url_img=plot_url_img, plot_url_img_cam=plot_url_img_cam, noticias_del_dia=noticias_del_dia, cursor3=cursor3)

	
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
    noticias_del_dia=cargaNoticias()
    return template("p_reporte.tpl", muni=muni, nivel=nivel,alta=alta, noticias_del_dia=noticias_del_dia)	


@post('/reporta')
def reporta():
 doc=etree.parse("static/Municipios/madrid.xml")
 muni=doc.findall("municipio")
 doc=etree.parse("static/Municipios/niveles.xml")
 nivel=doc.findall("nivel")
 reporte = {'municipio': request.POST['municipio'],
               'nivel_de_alerta': request.POST['nivel_de_alerta'],
               'realizada': datetime.datetime.now()}	
 print "municipio",  reporte['municipio']
 noticias_del_dia=cargaNoticias()
 if ((reporte['municipio']!='ninguno') and (reporte['nivel_de_alerta']!='ninguno')):	
    db.coleccion_reportes.insert(reporte)
    alta = 1
    varmun = str(reporte['municipio'])
    print type(varmun), "<---", type(reporte['municipio'])
    varniv = int(reporte['nivel_de_alerta'])
    print type(varniv), "<---", type(reporte['nivel_de_alerta'])
    #nuevoReporte(reporte['municipio'],reporte['nivel_de_alerta'])
    nuevoReporte(varmun,varniv)
    return template("p_reporte.tpl", muni=muni, nivel=nivel,alta=alta, noticias_del_dia=noticias_del_dia)	
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
    
      
    return template("error_views/p_reporte_error.tpl", muni=muni, nivel=nivel, nivsel=reporte['nivel_de_alerta'], munsel=reporte['municipio'], errores=listaErrores, noticias_del_dia=noticias_del_dia)



@route('/predicciones')
def predicciones():
    #from pymongo import MongoClient as Connection
    #cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    #MONGODB_URI =cadenaCon
    #conexion = Connection(MONGODB_URI)
    conexion=conexion_bbdd()
    db = conexion.othesoluciones1
    import gridfs
    fs = gridfs.GridFS(db)
    gridout = fs.get_last_version("ALERTAS.png")
    plot_url = base64.b64encode(gridout.read())
    noticias_del_dia=cargaNoticias()
    from pymongo import DESCENDING
    import datetime
    listaStrings = []
    listaPredicciones=[]
    hoy = (datetime.date.today()+datetime.timedelta(days=0)).strftime('%d-%m-%Y')
    listaStrings.append(hoy)
    stringHoy = 'Nivel '+hoy
    labelHoy = 'Alerta '+hoy
    #listaStrings.append(stringHoy)
    listaStrings.append(labelHoy)
    prediccionHoy = (db.PrediccionOTHE.find()
                .sort(stringHoy, DESCENDING)
                .limit(5))
    listaPredicciones.append(prediccionHoy)
    manana=(datetime.date.today()+datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    listaStrings.append(manana)
    stringManana = 'Nivel '+manana
    labelManana = 'Alerta '+manana
    #listaStrings.append(stringManana)
    listaStrings.append(labelManana)	
    prediccionManana = (db.PrediccionOTHE.find()
                .sort(stringManana, DESCENDING)
                .limit(5))
    listaPredicciones.append(prediccionManana)
    pasadomanana=(datetime.date.today()+datetime.timedelta(days=2)).strftime('%d-%m-%Y')
    listaStrings.append(pasadomanana)
    stringPasadoManana = 'Nivel '+pasadomanana
    labelPasadoManana = 'Alerta '+pasadomanana
    #listaStrings.append(stringPasadoManana)
    listaStrings.append(labelPasadoManana)
    prediccionPasadoManana = (db.PrediccionOTHE.find()
                .sort(stringPasadoManana, DESCENDING)
                .limit(5))
    listaPredicciones.append(prediccionPasadoManana)
    conexion.close()
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    #return template("p_predicciones.tpl", plot_url=plot_url,noticias_del_dia=noticias_del_dia, prediccionHoy=prediccionHoy, prediccionManana=prediccionManana, prediccionPasadoManana=prediccionPasadoManana, listaStrings=listaStrings, muni=muni)
    return template("p_predicciones.tpl", plot_url=plot_url,noticias_del_dia=noticias_del_dia, listaPredicciones=listaPredicciones, listaStrings=listaStrings, muni=muni)

	
	
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')
	
@error(404)
def error404(error):
    return 'Nothing here, sorry'


@get(['/notificaciones', '/notificaciones/:page#\d+#'])
@view('p_notificaciones')
def notificaciones(pageN=0):
    print "ENTRO POR AQUI"
    manana = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%d/%m/%Y')
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    alta=0
    ''' List messages. '''
    PAGE_SIZEN = 5
    pageN = int(pageN)
    prev_pageN = None
    if pageN > 0:
        prev_pageN = pageN - 1
    next_pageN = None
    if db.coleccion_notificaciones.count() > (pageN + 1) * PAGE_SIZEN:
        next_pageN = pageN + 1
    coleccion_notificaciones = (db.coleccion_notificaciones.find()
                .sort('realizada', DESCENDING)
                .limit(PAGE_SIZEN).skip(pageN * PAGE_SIZEN))
    noticias_del_dia=cargaNoticias()
    return {'coleccion_notificaciones': coleccion_notificaciones,
            'prev_pageN': prev_pageN,
            'next_pageN': next_pageN, 'alta':alta, 'muni':muni, 'fdesde':manana, 'fhasta':manana, 'noticias_del_dia':noticias_del_dia
            }	

# para PRO hay que ponerle 2 horas +
@post('/notifica')
def notifica():
 manana = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%d/%m/%Y')
 PAGE_SIZE = 5
 page = int(0)
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
 noticias_del_dia=cargaNoticias()
 if(cuentaErrores==0):
     alta=1
     db.coleccion_notificaciones.insert(notif)
     return template("p_notificaciones.tpl", muni=muni, alta=alta, coleccion_notificaciones=coleccion_notificaciones, prev_page=prev_page, next_page=next_page, fdesde=manana, fhasta=manana, noticias_del_dia=noticias_del_dia)	
 else:
  return template("error_views/p_notificaciones_error.tpl", muni=muni, errores=listaErrores, coleccion_notificaciones=coleccion_notificaciones, prev_page=prev_page, next_page=next_page, munsel=notif['municipio'], mailSel=mailSel, fdesde=notif['fdesde'], fhasta=notif['fhasta'], noticias_del_dia=noticias_del_dia )			
    
 #db.coleccion_notificaciones.insert(notif)
 #redirect('/notificaciones')

@post('/prediccion_muni')
def prediccion_muni():
    conexion=conexion_bbdd()
    db = conexion.othesoluciones1
    recibido= request.POST['municipio']
    codigo= recibido[0:5]
    name =  recibido[6:]
    listaStrings = []
    listaPredicciones=[]
    hoy = (datetime.date.today()+datetime.timedelta(days=0)).strftime('%d-%m-%Y')
    listaStrings.append(hoy)
    #stringHoy = 'Nivel '+hoy
    stringHoy = 'Alerta '+hoy
    listaStrings.append(stringHoy)
    prediccionHoy = (db.PrediccionOTHE.find_one({'Codigo':codigo}))
    listaPredicciones.append(prediccionHoy)
    manana=(datetime.date.today()+datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    listaStrings.append(manana)
    #stringManana = 'Nivel '+manana
    stringManana = 'Alerta '+manana
    listaStrings.append(stringManana)
    prediccionManana = (db.PrediccionOTHE.find_one({'Codigo':codigo}))
    listaPredicciones.append(prediccionManana)
    pasadomanana=(datetime.date.today()+datetime.timedelta(days=2)).strftime('%d-%m-%Y')
    listaStrings.append(pasadomanana)
    #stringPasadoManana = 'Nivel '+pasadomanana
    stringPasadoManana = 'Alerta '+pasadomanana
    listaStrings.append(stringPasadoManana)
    prediccionPasadoManana = (db.PrediccionOTHE.find_one({'Codigo':codigo}))
    listaPredicciones.append(prediccionPasadoManana)
	#Carga de imagenes del municipio
    collection2 = db.imagenes
    name2 =  elimina_tildes(name.decode('utf-8'))
    cursor2 = collection2.find_one({'municipio':name2})
    
    print prediccionHoy[stringHoy]
    if (prediccionHoy[stringHoy]=='Bajo'):
      f1 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio_bajo']) 
      plot_url_img = base64.b64encode(f1.read())
      f2 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio_cam_bajo']) 
      plot_url_img_cam = base64.b64encode(f2.read())		
    elif (prediccionHoy[stringHoy]=='Medio'):
           f1 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio_medio']) 
           plot_url_img = base64.b64encode(f1.read())
           f2 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio_cam_medio']) 
           plot_url_img_cam = base64.b64encode(f2.read())
    else:
           f1 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio_alto']) 
           plot_url_img = base64.b64encode(f1.read())
           f2 = gridfs.GridFS(db,"images").get_version(cursor2['filename_img_municipio_cam_alto']) 
           plot_url_img_cam = base64.b64encode(f2.read())	

		
		
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    noticias_del_dia=cargaNoticias()
    conexion.close()
    return template("p_predicciones_mun.tpl", name=name, noticias_del_dia=noticias_del_dia, listaPredicciones=listaPredicciones, listaStrings=listaStrings, plot_url_img=plot_url_img, plot_url_img_cam=plot_url_img_cam, muni=muni)	

	
cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
MONGODB_URI =cadenaCon
MONGODB_URI = 'mongodb://othesoluciones:othesoluciones@ds029635.mlab.com:29635/othesoluciones1'


db = Connection(MONGODB_URI).othesoluciones1

#Para ejecutar con BBDD local 
#db = Connection().othesoluciones1


run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
