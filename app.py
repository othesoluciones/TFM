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
    #Conexion BBDD
    conexion = conexion_bbdd()
    db = conexion.othesoluciones1
    ''' List noticias. '''
    PAGE_SIZE = 10
    noticias_del_dia = (db.noticias_del_dia.find().sort('Fecha de busqueda', DESCENDING).limit(PAGE_SIZE))
    #Conexion BBDD
    conexion.close()
    return noticias_del_dia	
	
#Pestana HOME
@get(['/'])
@view('index')
def index():
    #Conexion BBDD
	conexion = conexion_bbdd()
	db = conexion.othesoluciones1
	
	#Carga de la imagen ALERTAS.png
	import gridfs
	colorzona = gridfs.GridFS(db, "color-zona")
	gridout = colorzona.get_last_version("COLOR.png")
	plot_url_img = base64.b64encode(gridout.read())
	
	#Carga de noticias
	noticias_del_dia=cargaNoticias()
	
    #Conexion BBDD
	conexion.close()
	return {'noticias_del_dia': noticias_del_dia, 'plot_url_img':plot_url_img }		
	
#Pestana Niveles del dia
@get(['/hoy', '/hoy/:page#\d+#'])
@view('p_hoy')
def hoy(page=0):
    # CARGA DE NOTICIAS DEL DIA
    noticias_del_dia=cargaNoticias()
    #Conexion BBDD
    conexion = conexion_bbdd()
    db = conexion.othesoluciones1
	#Carga de la imagen ALERTAS.png
    import gridfs
    colorzona = gridfs.GridFS(db, "color-zona")
    gridout = colorzona.get_last_version("COLOR.png")
    plot_url = base64.b64encode(gridout.read())
    gridout_ley = colorzona.get_last_version("Leyenda.png")
    plot_url_ley = base64.b64encode(gridout_ley.read())
    ''' List messages. '''
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")

    import time
    hoy= time.strftime("%d-%m-%Y")
    listaZona1Texto=[]
    listaZona1Valor=[]
    listaZona2Texto=[]
    listaZona2Valor=[]
    listaZona3Texto=[]
    listaZona3Valor=[]
    listaZona4Texto=[]
    listaZona4Valor=[]
    listaZona5Texto=[]
    listaZona5Valor=[]
    listaZona6Texto=[]
    listaZona6Valor=[]	
    listaZona7Texto=[]
    listaZona7Valor=[]
    contZona1=0
    contZona2=0
    contZona3=0
    contZona4=0
    contZona5=0
    contZona6=0
    contZona7=0
	
    for i in (range(0,len(muni))):
		if(muni[i].attrib["zona"]=="1"):
			contZona1=contZona1+1
			listaZona1Texto.append(muni[i].text)
			listaZona1Valor.append("/"+muni[i].attrib["value"][-5:]+"/"+muni[i].text)
		elif(muni[i].attrib["zona"]=="2"):
			contZona2=contZona2+1
			listaZona2Texto.append(muni[i].text)
			listaZona2Valor.append("/"+muni[i].attrib["value"][-5:]+"/"+muni[i].text)
		elif(muni[i].attrib["zona"]=="3"):
			contZona3=contZona3+1
			listaZona3Texto.append(muni[i].text)
			listaZona3Valor.append("/"+muni[i].attrib["value"][-5:]+"/"+muni[i].text)
		elif(muni[i].attrib["zona"]=="4"):
			contZona4=contZona4+1
			listaZona4Texto.append(muni[i].text)
			listaZona4Valor.append("/"+muni[i].attrib["value"][-5:]+"/"+muni[i].text)
		elif(muni[i].attrib["zona"]=="5"):
			contZona5=contZona5+1
			listaZona5Texto.append(muni[i].text)
			listaZona5Valor.append("/"+muni[i].attrib["value"][-5:]+"/"+muni[i].text)
		elif(muni[i].attrib["zona"]=="6"):
			contZona6=contZona6+1
			listaZona6Texto.append(muni[i].text)
			listaZona6Valor.append("/"+muni[i].attrib["value"][-5:]+"/"+muni[i].text)
		else:
			contZona7=contZona7+1
			listaZona7Texto.append(muni[i].text)
			listaZona7Valor.append("/"+muni[i].attrib["value"][-5:]+"/"+muni[i].text)

    listaZona1=[]
    listaZona1.append(listaZona1Valor)
    listaZona1.append(listaZona1Texto)			
    listaZona2=[]
    listaZona2.append(listaZona2Valor)
    listaZona2.append(listaZona2Texto)
    listaZona3=[]
    listaZona3.append(listaZona3Valor)
    listaZona3.append(listaZona3Texto)	
    listaZona4=[]
    listaZona4.append(listaZona4Valor)
    listaZona4.append(listaZona4Texto)	
    listaZona5=[]
    listaZona5.append(listaZona5Valor)
    listaZona5.append(listaZona5Texto)	
    listaZona6=[]
    listaZona6.append(listaZona6Valor)
    listaZona6.append(listaZona6Texto)	
    listaZona7=[]
    listaZona7.append(listaZona7Valor)
    listaZona7.append(listaZona7Texto)		
    return {'noticias_del_dia': noticias_del_dia,'plot_url':plot_url, 'plot_url_ley':plot_url_ley, 'hoy':hoy,  'listaZona1':listaZona1,
            'muni': muni, 'listaZona2':listaZona2, 'listaZona3':listaZona3,'listaZona4':listaZona4,'listaZona5':listaZona5,'listaZona6':listaZona6,'listaZona7':listaZona7
            }	


#Pestana Niveles del dia - Carga de datos del municipio			
@get(['/<cod>/<name>'])
@view('p_hoy_mun')
def hoy_mun(cod,name):
    import datetime
    import time
    import json

	
    #Conexion BBDD
    conexion = conexion_bbdd()
    db = conexion.othesoluciones1
	
	#Redireccion en la paginacion de la pagina de reportes
    if (cod=='reporte'):
      return reporte(name)
	  
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
	
    #Conexion BBDD
    conexion.close()	
	
    return template("p_hoy_mun.tpl",name=name, busquedaAEMET=busquedaAEMET,plot_url_img=plot_url_img, plot_url_img_cam=plot_url_img_cam, noticias_del_dia=noticias_del_dia, cursor3=cursor3)

#Pestana Predicciones
@route('/predicciones')
def predicciones():
    #Conexion BBDD
    conexion=conexion_bbdd()
    db = conexion.othesoluciones1

	#Carga de noticias
    noticias_del_dia=cargaNoticias()
	
	#Carga de la imagen ALERTAS.png	
    import gridfs
    fs = gridfs.GridFS(db)
    gridout = fs.get_last_version("ALERTAS.png")
    plot_url = base64.b64encode(gridout.read())

	#Buscamos en BBDD para cada uno de los 3 proximos dias los 5 municipios con mayor nivel de alerta
    from pymongo import DESCENDING
    import datetime
	#listaStrings -> lista que almacena la fecha del dia y el campo por el que vamos a filtrar en la pagina
    listaStrings = []
	#listaPredicciones -> lista que almacena cada uno de los resultados de la busqueda por el dia
    listaPredicciones=[]
	
	#Bloque busqueda de hoy
    hoy = (datetime.date.today()+datetime.timedelta(days=0)).strftime('%d-%m-%Y')
    listaStrings.append(hoy)
    labelHoy = 'Alerta '+hoy
    listaStrings.append(labelHoy)
    stringHoy = 'Nivel '+hoy
    prediccionHoy = (db.PrediccionOTHE.find()
                .sort(stringHoy, DESCENDING)
                .limit(5))
    listaPredicciones.append(prediccionHoy)
	
	#Bloque busqueda de manana
    manana=(datetime.date.today()+datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    listaStrings.append(manana)
    labelManana = 'Alerta '+manana
    listaStrings.append(labelManana)	
    stringManana = 'Nivel '+manana
    prediccionManana = (db.PrediccionOTHE.find()
                .sort(stringManana, DESCENDING)
                .limit(5))
    listaPredicciones.append(prediccionManana)

	#Bloque busqueda de pasado manana
    pasadomanana=(datetime.date.today()+datetime.timedelta(days=2)).strftime('%d-%m-%Y')
    listaStrings.append(pasadomanana)
    labelPasadoManana = 'Alerta '+pasadomanana
    listaStrings.append(labelPasadoManana)
    stringPasadoManana = 'Nivel '+pasadomanana
    prediccionPasadoManana = (db.PrediccionOTHE.find()
                .sort(stringPasadoManana, DESCENDING)
                .limit(5))
    listaPredicciones.append(prediccionPasadoManana)
	
    #Conexion BBDD	
    conexion.close()
	
	#Carga de los combos desde los xml
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
   
    return template("p_predicciones.tpl", plot_url=plot_url,noticias_del_dia=noticias_del_dia, listaPredicciones=listaPredicciones, listaStrings=listaStrings, muni=muni)
	
#Acciones a realizar tras pulsar sobre el formulario de la pestana Predicciones -> redirige a Predicciones y prediccion_mun	
@post('/prediccion_muni')
def prediccion_muni():
    #Conexion BBDD
    conexion=conexion_bbdd()
    db = conexion.othesoluciones1

	#Carga de noticias
    noticias_del_dia=cargaNoticias()
	
	#Parseamos el valor del munipio
    recibido= request.POST['municipio']
    codigo= recibido[0:5]
    name =  recibido[6:]
	
    import datetime
	#listaStrings -> lista que almacena la fecha del dia y el campo por el que vamos a filtrar en la pagina	
    listaStrings = []
	
	#listaPredicciones -> lista que almacena cada uno de los resultados de la busqueda por el dia	
    listaPredicciones=[]

	#Bloque busqueda de hoy
    hoy = (datetime.date.today()+datetime.timedelta(days=0)).strftime('%d-%m-%Y')
    listaStrings.append(hoy)
    stringHoy = 'Alerta '+hoy
    listaStrings.append(stringHoy)
    prediccionHoy = (db.PrediccionOTHE.find_one({'Codigo':codigo}))
    listaPredicciones.append(prediccionHoy)
	
	#Bloque busqueda de manana	
    manana=(datetime.date.today()+datetime.timedelta(days=1)).strftime('%d-%m-%Y')
    listaStrings.append(manana)
    stringManana = 'Alerta '+manana
    listaStrings.append(stringManana)
    prediccionManana = (db.PrediccionOTHE.find_one({'Codigo':codigo}))
    listaPredicciones.append(prediccionManana)
	
	#Bloque busqueda de pasado manana	
    pasadomanana=(datetime.date.today()+datetime.timedelta(days=2)).strftime('%d-%m-%Y')
    listaStrings.append(pasadomanana)
    stringPasadoManana = 'Alerta '+pasadomanana
    listaStrings.append(stringPasadoManana)
    prediccionPasadoManana = (db.PrediccionOTHE.find_one({'Codigo':codigo}))
    listaPredicciones.append(prediccionPasadoManana)
	
	#Buscamos en imagenes los tags por los que vamos a buscar en funcion del nivel de alerta del municipio
    collection2 = db.imagenes
    name2 =  elimina_tildes(name.decode('utf-8'))
    cursor2 = collection2.find_one({'municipio':name2})
    
	#Obtenemos las imagenes correctas de los municipios
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

    #Conexion BBDD		
    conexion.close()
    return template("p_predicciones_mun.tpl", name=name, noticias_del_dia=noticias_del_dia, listaPredicciones=listaPredicciones, listaStrings=listaStrings, plot_url_img=plot_url_img, plot_url_img_cam=plot_url_img_cam)	

#Pestana Reportanos	
@route('/reporte')
def reporte(page=0):
    #Conexion BBDD
    conexion = conexion_bbdd()
    db = conexion.othesoluciones1   

	#Carga de las noticias del dia
    noticias_del_dia=cargaNoticias()
	
	#Carga de los combos desde los xml
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    doc=etree.parse("static/Municipios/niveles.xml")
    nivel=doc.findall("nivel")
	
	#Flag para mostrar mensaje de alta correcta o no
    alta = 0

    #Paginacion
    ''' List messages. '''
    PAGE_SIZE = 5
    page = int(page)
    prev_page = None
    if page > 0:
        prev_page = page - 1
    next_page = None
    cuantosReportes = db.coleccion_reportes.find({'realizada':hoy}).count()
    hoy=datetime.datetime.now().strftime('%d-%m-%Y')
    if db.coleccion_reportes.find({'realizada':hoy}).count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    coleccion_reportes = (db.coleccion_reportes.find({'realizada':hoy})
                .sort('hora', DESCENDING)
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE)) 

    #Conexion BBDD
    conexion.close()					
    return template("p_reporte.tpl", muni=muni, nivel=nivel,alta=alta, noticias_del_dia=noticias_del_dia, prev_page=prev_page, next_page=next_page, coleccion_reportes=coleccion_reportes, hoy=hoy, cuantosReportes=cuantosReportes)	

#Acciones a realizar tras pulsar sobre el formulario de la pestana Reportanos -> redirige a Reportanos y p_reporte_error
@post('/reporta')
def reporta():
 #Carga de los combos desde los xml y establecemos la etiqueta que mostraremos en funcion del valor de la alerta reportada
 doc=etree.parse("static/Municipios/madrid.xml")
 muni=doc.findall("municipio")
 doc=etree.parse("static/Municipios/niveles.xml")
 nivel=doc.findall("nivel")
 if (request.POST['nivel_de_alerta']=='0'):
    labelAlerta='Bajo'
 elif (request.POST['nivel_de_alerta']=='1'):
     labelAlerta='Medio'
 else:
     labelAlerta='Alto'
 
 #Carga del nombre del municipio desde el xml (con acentos)
 i=0
 encontrado=False  
 indice=0
 while( (i<len(muni)) and (encontrado==False)):
    if (muni[i].attrib["value"][-5:]==request.POST['municipio']):
        encontrado=True
        indice=i
    i=i+1
 from datetime import timedelta
 hora=(datetime.datetime.now() + timedelta(hours=2)).strftime('%H:%M:%S')

 #Diccionario que vamos a insertar en la BBDD 
 reporte = {'municipio': request.POST['municipio'], 'municipio_label':muni[indice].text,
               'nivel_de_alerta': request.POST['nivel_de_alerta'],
			   'labelAlerta':labelAlerta,
               'realizada': datetime.datetime.now().strftime('%d-%m-%Y'), 'hora': hora}	
 print "municipio",  reporte['municipio']
 
 
 #Carga de las noticias del dia
 noticias_del_dia=cargaNoticias()

 #Conexion BBDD
 conexion = conexion_bbdd()
 db = conexion.othesoluciones1
 ''' List messages. '''
 PAGE_SIZE = 5
 prev_page = None
 page=0
 if page > 0:
        prev_page = page - 1
 next_page = None
 hoy=datetime.datetime.now().strftime('%d-%m-%Y')
 cuantosReportes = db.coleccion_reportes.find({'realizada':hoy}).count()
 if db.coleccion_reportes.find({'realizada':hoy}).count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
 coleccion_reportes = (db.coleccion_reportes.find({'realizada':hoy})
                .sort('hora', DESCENDING)
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE)) 
 
 if ((reporte['municipio']!='ninguno') and (reporte['nivel_de_alerta']!='ninguno')):	
    #Formulario rellenado correctamente
	
	#Insert del reporte
    db.coleccion_reportes.insert(reporte)
	
	#Flag activado para mostrar mensaje de alta OK
    alta = 1
	
	#Llamada a la funcion nuevoReporte para actualizar la tabla de Predicciones 
    varmun = str(reporte['municipio'])
    varniv = int(reporte['nivel_de_alerta'])
    nuevoReporte(varmun,varniv)	
  
	#Actualizacion de la paginacion 
    ''' List messages. '''
    PAGE_SIZE = 5
    prev_page = None
    page=0
    if page > 0:
        prev_page = page - 1
    next_page = None
    hoy=datetime.datetime.now().strftime('%d-%m-%Y')
    if db.coleccion_reportes.find({'realizada':hoy}).count() > (page + 1) * PAGE_SIZE:
        next_page = page + 1
    coleccion_reportes = (db.coleccion_reportes.find({'realizada':hoy})
                .sort('hora', DESCENDING)
                .limit(PAGE_SIZE).skip(page * PAGE_SIZE))
				
    #Conexion BBDD
    conexion.close()	
	
    return template("p_reporte.tpl", muni=muni, nivel=nivel,alta=alta, noticias_del_dia=noticias_del_dia, prev_page=prev_page, next_page=next_page, coleccion_reportes=coleccion_reportes, hoy=hoy,  cuantosReportes=cuantosReportes)			

 else:
    # Tratamos los errores en el envio del formulario
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
    
      
    return template("error_views/p_reporte_error.tpl", muni=muni, nivel=nivel, nivsel=reporte['nivel_de_alerta'], munsel=reporte['municipio'], errores=listaErrores, noticias_del_dia=noticias_del_dia, prev_page=prev_page, next_page=next_page, coleccion_reportes=coleccion_reportes, hoy=hoy,  cuantosReportes=cuantosReportes)		

#Pestana Notificaciones	
@get(['/notificaciones'])
@view('p_notificaciones')
def notificaciones():
	#Carga de noticias
    noticias_del_dia=cargaNoticias()
	
	#Obtenemos la fecha de manana para inicializar los campos fechadesde y fechahasta
    import datetime	
    manana = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%d/%m/%Y')

	#Carga de los combos desde los xml	
    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
	
	#Flag para mostrar mensaje de alta correcta o no	
    alta=0    

    return { 'alta':alta, 'muni':muni, 'fdesde':manana, 'fhasta':manana, 'noticias_del_dia':noticias_del_dia }	

#Acciones a realizar tras pulsar sobre el formulario de la pestana Notificaciones -> redirige a Notificaciones y p_notificaciones_error
@post('/notifica')
def notifica():
 #Carga de noticias
 noticias_del_dia=cargaNoticias()
 
 #Carga de los combos desde los xml	 
 doc=etree.parse("static/Municipios/madrid.xml")
 muni=doc.findall("municipio") 
 
 #Obtenemos las fechas en el formato que queremos desde el formulario
 import datetime
 fechaHastaIns= datetime.datetime.strptime(request.POST['fechaHasta'],'%d/%m/%Y')
 fechaDesdeIns= datetime.datetime.strptime(request.POST['fechaDesde'],'%d/%m/%Y')
 
 #Diccionario que almacena los campos recibidos del formulario 
 notif = {'email': request.POST['email'], 'fdesde':request.POST['fechaDesde'], 'fhasta':request.POST['fechaHasta'],
               'municipio': request.POST['municipio'],
               'realizada': datetime.datetime.now()}

 #listaErrores -> es una lista de booleanos donde vamos a almacenar si los 3 campos del formulario se han rellenado correctamente o no			   
 listaErrores=[]			   
 
 #Validacion Email
 import re
 email_address = request.POST['email']
 #Comprobamos que el email cumple los requerimientos minimos
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
 
 #Validamos municipio	
 if (notif['municipio']=='ninguno'):
  municipio_OK=False
 else:
  municipio_OK=True
 listaErrores.append(municipio_OK)
 
 #Validamos las fechas
 if ((notif['fdesde']=='')or(notif['fdesde']=='')):
  fechas_OK=False
 else:
  fechas_OK=True
  
 listaErrores.append(fechas_OK) 
 
 #En cuentaErrores contamos el numero de falses introducidos para ver si se ha rellenado el formulario correctamente o no y asi redirigir la navegacion correctamente
 cuentaErrores= listaErrores.count(False)

 #Sin errores
 if(cuentaErrores==0):
     alta=1
     db.coleccion_notificaciones.insert(notif)
     #Obtenemos la fecha de manana para inicializar los campos fechadesde y fechahasta para en caso de exito cargarlas en la pantalla inicial de notificaciones
     manana = (datetime.date.today()+datetime.timedelta(days=1)).strftime('%d/%m/%Y')
     return template("p_notificaciones.tpl", muni=muni, alta=alta, fdesde=manana, fhasta=manana, noticias_del_dia=noticias_del_dia)	
 else:
  #Con errores
  return template("error_views/p_notificaciones_error.tpl", muni=muni, errores=listaErrores, munsel=notif['municipio'], mailSel=mailSel, fdesde=notif['fdesde'], fhasta=notif['fhasta'], noticias_del_dia=noticias_del_dia )			
    
#Obtencion de los estaticos de la carpeta /static
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')
	
#Pantalla de error	
@error(404)
def error404(error):
    return 'Nothing here, sorry'

	
cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
MONGODB_URI =cadenaCon
MONGODB_URI = 'mongodb://othesoluciones:othesoluciones@ds029635.mlab.com:29635/othesoluciones1'


db = Connection(MONGODB_URI).othesoluciones1

#Para ejecutar con BBDD local 
#db = Connection().othesoluciones1


run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
