import os
import time
import base64
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import datetime
import unicodedata

logging.basicConfig()

scheduler = BlockingScheduler()

def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
   
   
def envioMail():
 print "Comenzamos envio mail"
 from email.mime.multipart import MIMEMultipart
 from email.mime.text import MIMEText
 from email.mime.image import MIMEImage
 # Establecemos conexion con el servidor smtp de gmail
 mailServer = smtplib.SMTP('smtp.gmail.com',587)
 mailServer.ehlo()
 mailServer.starttls()
 mailServer.ehlo()
 password = base64.b64decode("Q29uc3RhbmNpYTIx")
 mailServer.login("othesoluciones@gmail.com",password)
 # Construimos un mensaje Multipart, con un texto y una imagen adjunta

 cuentaDesde = "othesoluciones@gmail.com"
 cuentaPara = "cesarhernandez@campusciff.net"
 mensaje = MIMEMultipart()
 mensaje['From']=cuentaDesde
 mensaje['To']=cuentaPara
 mensaje['Subject']="Tienes un correo"

# Adjuntamos el texto
 html = """\
 <html>
  <head></head>
  <body>
      <p>Hola,</p>
      <p>Este es el cuerpo del correo. Y sale el logo!</p>
      <p>---</p>
      <img src="cid:logo" alt="Othe Soluciones" height="52" width="52"></img>
 </html>"""

 mensaje.attach(MIMEText(html,'html'))
 # Adjuntamos la imagen
 file = open("logo.jpg", "rb")
 contenido = MIMEImage(file.read())
 contenido.add_header('Content-ID', '<logo>')
 mensaje.attach(contenido)
 # Enviamos el correo, con los campos from y to.
 mailServer.sendmail(cuentaDesde, cuentaPara, mensaje.as_string())
 # Cierre de la conexion
 mailServer.close()
 print "Enviado"
 
def actualiza_calidad_aire():
     # Para todas las localidades
    import time
    import json
    import urllib
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup

    #Conectamos a la base de datos
    import base64
    from pymongo import MongoClient as Connection
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1

    primeraVez = True

    for i in range (2,8):
        link ="http://gestiona.madrid.org/azul_internet/html/web/DatosZonaAccion.icm?ESTADO_MENU=2&idZona="
        link+=`i`
        url = urllib.urlopen(link)
        myfile = url.read()
        soup = BeautifulSoup(myfile)

        #HORA
        if primeraVez:
            horas = soup.find_all("td", class_="txt08gr3", id="fondoVainilla")
            horas[0].text
            start =horas[0].text.find('(')+1
            end = horas[0].text.find(')',start)
            hora = horas[0].text[start:end]

            primeraVez = False

        valores = []

        #ESTACIONES
        estaciones =[]
        for est in soup.find_all("a", class_="txt06roj"):
            start =est.text.find('idEstacion=')+11
            end = est.text.find('"',start)
            estacion = est.text[start:end].strip()
            estaciones.append(estacion)
        estaciones=filter(None, estaciones)
        estaciones = sorted(set(estaciones))

        #COLUMNAS
        metricas = soup.find_all("td", class_="txt07neg",id="fondoGris")
        columnas=[]
        for k in range(len(metricas)):
            col = elimina_tildes(unicode(metricas[k].strong.a['title']))
            columnas.append(col.upper())

        for tabla in soup.findAll("table",align="center"):
            for dato in tabla.find_all("td", class_="txt07neg", align="right"):
                valores.append(dato.get_text().strip())
        j=0
        numContaminantes = len(soup.find("table",align="center").find_all("td", class_="txt07neg",id="fondoGris"))
        numParamMeteor = len(columnas) - numContaminantes

        lista1=[]
        lista2=[]

        while j<len(valores):
            if j< numContaminantes*len(estaciones):
                lista1.append(valores[j:j+numContaminantes])
                j+=numContaminantes
            else:
                lista2.append(valores[j:j+numParamMeteor])  
                j+=numParamMeteor

        lista3 = [a + b for a, b in zip(lista1, lista2)]

        df=pd.DataFrame(lista3,columns=columnas)
        df['Estacion'] = estaciones

        #Dia actual
        dia = time.strftime("%d/%m/%Y")
        df['Dia']=dia
        df['Hora']=hora
        df['Zona']=i
        
        df.rename(columns=lambda x: x.replace('.', ''), inplace=True)
        df.columns

        recordsdf = json.loads(df.T.to_json()).values()
        db.calidad_aire.insert_many(recordsdf)
        
    conexion.close() 

 
def noticias_del_dia():
    print "Empezamos metodo noticias_deldia"
    #Conectamos a la base de datos
    import base64
    import json
    from pymongo import MongoClient as Connection
    from bs4 import BeautifulSoup
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    #MONGODB_URI = 'mongodb://othesoluciones:othesoluciones@ds029635.mlab.com:29635/othesoluciones1'
    # db = Connection(MONGODB_URI).othesoluciones1 
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1

    
    from googleapiclient.discovery import build
    import time
    import pandas as pd

    my_api_key = "AIzaSyDJsXbW0d6P0WzMKvKWOgs94UzJnK98izQ"
    my_cse_id = "006049000923477598507:r2tzp5mrnc8"

    #Dia actual
    dia = time.strftime("%d/%m/%Y")


    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        return res['items']

    results = google_search(
        'polen Madrid 2016', my_api_key, my_cse_id, num=10)
    noticias = []
    titulo = []
    fecha = []
    for result in results:
        noticias.append(result["link"])
        titulo.append(BeautifulSoup(result["htmlTitle"]).text)
        fecha.append(dia)

    df=pd.DataFrame()
    df['Noticia']=noticias
    df['Titulo']=titulo
    df['Fecha de busqueda']=fecha
    recordsdf = json.loads(df.T.to_json()).values()
    db.noticias_del_dia.insert_many(recordsdf)
    conexion.close()  
    print "Finalizado metodo noticias_deldia"
	
def prediccionAEMET (xmlUrl,municipio,CP):
    #Crea un diccionario para cada municipio con la informacion que deseamos almacenar.
    import urllib
    import xmltodict
    file = urllib.urlopen(xmlUrl)
    data = file.read()
    file.close()

    data = xmltodict.parse(data)

    diccionario = {}
    diccionario['Municipio']=municipio
    #diccionario['link_xml']=xmlUrl
    #diccionario['Codigo_Postal']=CP
    #diccionario[municipio]={}
    for dia in data['root']['prediccion']['dia']:
        diccionario[dia['@fecha']]=[]
        #diccionario[municipio][dia['@fecha']]={}
        dicFech ={}
        tamPrecip = len(dia['prob_precipitacion'])
        if type(dia['prob_precipitacion']) ==list:
            for periodo in dia['prob_precipitacion']:
                if  len(periodo)>1:
                    dicFech['precipitaciones '+periodo['@periodo']]=periodo.items()[1][1]
                    #diccionario[municipio][dia['@fecha']]['precipitaciones '+periodo['@periodo']]=periodo.items()[1][1] #periodo['#text']          
        else:
            #diccionario[municipio][dia['@fecha']]['precipitaciones']=dia['prob_precipitacion']
            dicFech['precipitaciones']=dia['prob_precipitacion']
        tamViento = len(dia['viento'])  
        if tamViento>2:
            for viento in dia['viento']:
                if  len(viento)>1:
                    #diccionario[municipio][dia['@fecha']]['viento '+viento['@periodo']]= viento['velocidad']
                    dicFech['viento '+viento['@periodo']]= viento['velocidad']
        else:
            #diccionario[municipio][dia['@fecha']]['viento']= viento['velocidad']
            dicFech['viento']= viento['velocidad']
        #diccionario[municipio][dia['@fecha']]['Temperatura maxima']= dia['temperatura']['maxima']
        #diccionario[municipio][dia['@fecha']]['Temperatura minima']= dia['temperatura']['minima']
        dicFech['Temperatura maxima']= dia['temperatura']['maxima']
        dicFech['Temperatura minima']= dia['temperatura']['minima']
        tamTemp=len(dia['temperatura'])  
        if tamTemp>2:
            for temp in dia['temperatura']['dato']:
                if len(temp)>1:
                 #diccionario[municipio][dia['@fecha']]['Temperatura '+temp['@hora']]= temp.items()[1][1] #temp['#text'] 
                 dicFech['Temperatura '+temp['@hora']]= temp.items()[1][1]
        #diccionario[municipio][dia['@fecha']]['Humedad relativa maxima']= dia['humedad_relativa']['maxima']
        #diccionario[municipio][dia['@fecha']]['Humedad relativa minima']= dia['humedad_relativa']['minima'] 
        dicFech['Humedad relativa maxima']= dia['humedad_relativa']['maxima']
        dicFech['Humedad relativa minima']= dia['humedad_relativa']['minima'] 
        tamHum=len(dia['humedad_relativa'])  
        if tamHum>2:
            for temp in dia['humedad_relativa']['dato']:
              if len(temp)>1:
                 #diccionario[municipio][dia['@fecha']]['Humedad relativa '+temp['@hora']]= temp.items()[1][1]#temp['#text']    
                 dicFech['Humedad relativa '+temp['@hora']]= temp.items()[1][1]
        diccionario[dia['@fecha']].append(dicFech)
    return diccionario

def prediccionesAEMET():
    import urllib
    import xmltodict
    from bs4 import BeautifulSoup

    url = "http://www.aemet.es/es/eltiempo/prediccion/municipios?p=28&w=t"
    f = urllib.urlopen(url)
    myfile = f.read()
    soup = BeautifulSoup(myfile)

    #Conectamos a la base de datos
    import base64
    import json
    from pymongo import MongoClient as Connection
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1
    db.prediccionesAEMET.drop()

    for urls in soup.find_all('td'):
        localidad = urls.a.text
        time.sleep(1)
        url = "http://www.aemet.es"+urls.a['href']

        r = urllib.urlopen(url).read()

        soup = BeautifulSoup(r)

        #Enlace a los xml con las predicciones
        localidad = elimina_tildes(localidad)
        xmlLink = soup.find_all('div', class_="enlace_xml")
        print "Empezamos",datetime.datetime.now()," -->", localidad
        for xml in xmlLink:
            xmlUrl= "http://www.aemet.es"+xml.a['href'] 
            CP=  xml.a['href'].split('_')[1][:5] 
        pred=prediccionAEMET (xmlUrl,localidad,CP)
        print "Terminamos -->", localidad
        db.prediccionesAEMET.insert_one(pred)
        #time.sleep(10)
    print "fin"
    conexion.close()  
	
	
def NivelesPolenMadrid():
    import pandas as pd
    import numpy as np
    import urllib
    from bs4 import BeautifulSoup
    print "Empezamos metodo nivelespolenmadrid"
     #Conectamos a la base de datos
    import base64
    import json
    from pymongo import MongoClient as Connection
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1

    link ="http://polenes.com/graficos/jsp/ImgGrafico.jsp?chkSelTodos=on&chkPolenes=CUPRE&chkPolenes=PALMA&chkPolenes=RUMEX&chkPolenes=MERCU&chkPolenes=MORUS&chkPolenes=URTIC&chkPolenes=ALNUS&chkPolenes=BETUL&chkPolenes=CAREX&chkPolenes=FRAXI&chkPolenes=QUERC&chkPolenes=OLEA&chkPolenes=PINUS&chkPolenes=ULMUS&chkPolenes=CASTA&chkPolenes=POPUL&chkPolenes=GRAMI&chkPolenes=QUEAM&chkPolenes=PLATA&chkPolenes=PLANT&chkPolenes=ARTEM&chkPolenes=ALTER&selEstacion=MAD&selAnioTrimes=&selPeriodo=USE&txtFDesde=01%2F01%2F2010&txtFHasta=12%2F08%2F2016&prov=MAD&hidPolen=%26polen%3DCUPRE%26polen%3DPALMA%26polen%3DRUMEX%26polen%3DMERCU%26polen%3DMORUS%26polen%3DURTIC%26polen%3DALNUS%26polen%3DBETUL%26polen%3DCAREX%26polen%3DFRAXI%26polen%3DQUERC%26polen%3DOLEA%26polen%3DPINUS%26polen%3DULMUS%26polen%3DCASTA%26polen%3DPOPUL%26polen%3DGRAMI%26polen%3DQUEAM%26polen%3DPLATA%26polen%3DPLANT%26polen%3DARTEM%26polen%3DALTER&hidCheckSel=&mostrarGraf=S&hidPolenSolo=N&idio=ES&numPolenesSeleccionados=22&hidAniosEstacion=&primero=trueutm_source=twitter&utm_medium=twitter&utm_campaign=twitter"
    f = urllib.urlopen(link)
    myfile = f.read()

    soup = BeautifulSoup(myfile)

    tabla = soup.findAll("table")[1]
    datos = []

    for dato in tabla.find_all("td"):
        datos.append(dato.get_text().strip())

    datos.pop(0)
    valores = [s for s in datos if s.isdigit()]

    #Calculamos la posicion del primer valor numerico
    ind =0
    primerValor=0
    for s in datos:
        ind+=1
        if s.isdigit() and primerValor==0:
            primerValor=ind

    columnas =[]
    for i in range(primerValor-2):
        if len(datos[i].split("\n"))>1:
            columnas.append(datos[i].split("\n")[1])
        else:
            columnas.append(datos[i])

    tamColumnas = len(columnas)
    k=primerValor-2
    lista = []
    while k<len(datos):
        lista.append(datos[k:k+tamColumnas])
        k+=tamColumnas

    df=pd.DataFrame(lista,columns=columnas)
    recordsdf = json.loads(df.T.to_json()).values()
    db.nivelesPolenSEAIC.insert_many(recordsdf)
    conexion.close()
    print "Terminado metodo nivelespolenmadrid"

def algoritmoPredictivo():
    #Lee de la base de datos
    import base64
    import json
    from pymongo import MongoClient as Connection
    import datetime
    import string
    from lxml import etree
    
    cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
    MONGODB_URI =cadenaCon
    conexion = Connection(MONGODB_URI)
    db = conexion.othesoluciones1

    #Calculamos el mes y la semana actual
    mes = datetime.date.today().month
    semana = datetime.date.today().isocalendar()[1]

    #Obtenemos el nivel inicial
    NivelBase=db.calendarioPolen.find_one({"Mes": mes})['Nivel']

    #Obtenemos el nivel proporcionado por el nivel de polen
    NivelPolen =db.nivelesPolenSEAIC.find_one({"$and": [{"Polen/Fecha":"Gramineas"},{"Semana": semana}]})["Nivel"]

    if NivelBase<NivelPolen:
        NivelBase = NivelBase+0.5
    else:
        if NivelBase>NivelPolen:
            NivelBase = NivelBase-0.5
   
    #Leemos de la base de datos la coleccion de Calidad del Aire estableciendo una puntuacion para cada zona.

    dia = datetime.date.today().strftime('%d/%m/%Y')

    colEst=[]
    colZona=[]
    colNO2=[]
    colPM10=[]
    colPM25=[]
    colCO=[]
    colO3=[]
    colSO2=[]
    colNO=[]
    colNIVEL=[]
    for cursor in db.calidad_aire.find({'Dia':dia}):
        nivel=0
        colEst.append(cursor['Estacion'])
        colZona.append(cursor['Zona'])
        colNO2.append(cursor['DIOXIDO DE NITROGENO'])
        if cursor['DIOXIDO DE NITROGENO'].isdigit() and int(cursor['DIOXIDO DE NITROGENO'])>200:
            nivel+=0.1
        colPM10.append(cursor['PARTICULAS EN SUSPENSION < PM10'])
        if cursor['PARTICULAS EN SUSPENSION < PM10'].isdigit() and int(cursor['PARTICULAS EN SUSPENSION < PM10'])>50:
            nivel+=0.1
        colPM25.append(cursor['PARTICULAS EN SUSPENSION < PM2,5'])
        if cursor['PARTICULAS EN SUSPENSION < PM2,5'].isdigit() and int(cursor['PARTICULAS EN SUSPENSION < PM2,5'])>25:
            nivel+=0.1
        colCO.append(cursor['MONOXIDO DE CARBONO'])
        if cursor['MONOXIDO DE CARBONO'].isdigit() and int(cursor['MONOXIDO DE CARBONO'])>10:
            nivel+=0.1
        colO3.append(cursor['CONCENTRACION DE OZONO'])
        if cursor['CONCENTRACION DE OZONO'].isdigit() and int(cursor['CONCENTRACION DE OZONO'])>120:
            nivel+=0.1
        colSO2.append(cursor['DIOXIDO DE AZUFRE'])
        if cursor['DIOXIDO DE AZUFRE'].isdigit() and int(cursor['DIOXIDO DE AZUFRE'])>350:
            nivel+=0.1
        colNO.append(cursor['MONOXIDO DE NITROGENO'])
        if cursor['MONOXIDO DE NITROGENO'].isdigit() and int(cursor['MONOXIDO DE NITROGENO'])>30:
            nivel+=0.1

        colNIVEL.append(nivel)

    dfCalidadAire=pd.DataFrame()

    dfCalidadAire['ZONA']=colZona
    dfCalidadAire['NO2']=colNO2
    dfCalidadAire['PM10']=colPM10
    dfCalidadAire['PM25']=colPM25
    dfCalidadAire['CO']=colCO
    dfCalidadAire['O3']=colO3
    dfCalidadAire['SO2']=colSO2
    dfCalidadAire['NO']=colNO
    dfCalidadAire['NIVEL']=colNIVEL

    tamDF =db.calidad_aire.find({'Dia':dia}).count()
    nivMax = dfCalidadAire['NIVEL'].max()

    dfCalidadAire.loc[tamDF] = [1,0,0,0,0,0,0,0,nivMax]

    #Calculamos la media por zona
    dfNivel = dfCalidadAire[['ZONA','NIVEL']]
    dfMEDIA=dfNivel.groupby(by='ZONA').mean()
    #Leemos del xml de Madrid para asociar a cada municipio con su zona.

    doc=etree.parse("static/Municipios/madrid.xml")
    muni=doc.findall("municipio")
    municipio=[]
    zona=[]
    codigo=[]
    for localidad in muni:
        zona.append(localidad.get('zona'))
        municipio.append(elimina_tildes(unicode(localidad.text)))
        codigo.append(localidad.get('value').split('id')[1])
    dfMun=pd.DataFrame()
    dfMun['Municipio']=municipio
    dfMun['Zona']=zona
    dfMun['Codigo']=codigo

    #Anyadimos los datos de predicciones AEMET al modelo
    Municipios=[]
    Zona=[]
    nivelCalidad=[]
    nivelesAEMET1=[]
    nivelesAEMET2=[]
    nivelesAEMET3=[]
    codigoP=[]
    dia1 = datetime.date.today()
    dia2 = datetime.date.today() + datetime.timedelta(days=1)
    dia3 = datetime.date.today() + datetime.timedelta(days=2)

    dias=[dia1.strftime("%Y-%m-%d"),dia2.strftime("%Y-%m-%d"),dia3.strftime("%Y-%m-%d")]
    dia1F = dia1.strftime('%d-%m-%Y')
    dia2F = dia2.strftime('%d-%m-%Y')
    dia3F = dia3.strftime('%d-%m-%Y')

    for pred in db.prediccionesAEMET.find():
        Municipios.append(pred['Municipio'])
        valZona = string.join(dfMun[dfMun.Municipio.isin([pred['Municipio']])]['Zona'].values)

        nivelCalidad.append(dfMEDIA.ix[int(valZona)]['NIVEL'])
        codigoP.append(string.join(dfMun[dfMun.Municipio.isin([pred['Municipio']])]['Codigo'].values))
        Zona.append(valZona)

        for indice in range(len(dias)):
            nivelAEMETDia=0
            for predaux in pred[dias[indice]]:

                if predaux['viento 00-24']>30:
                    nivelAEMETDia+=0.3
                if predaux['precipitaciones 00-24']>30:
                    nivelAEMETDia-=0.2
                if predaux['Humedad relativa minima']>40:
                    nivelAEMETDia-=0.1
                if predaux['Humedad relativa maxima']>70:
                    nivelAEMETDia-=0.1
                if predaux['Temperatura minima']>20:
                    nivelAEMETDia+=0.1
                if predaux['Temperatura maxima']>30:
                    nivelAEMETDia+=0.1
            if indice==0:
                nivelesAEMET1.append(nivelAEMETDia)
            else:
                if indice==1:
                     nivelesAEMET2.append(nivelAEMETDia)
                else:
                     nivelesAEMET3.append(nivelAEMETDia)
                        
    #Creamos un nuevo df con las predicciones calculadas.
    dfPredAEMET=pd.DataFrame()
    dfPredAEMET['Municipio']=Municipios
    dfPredAEMET['Codigo']=codigoP
    dfPredAEMET['Nivel Base']=NivelBase
    dfPredAEMET['Plus Calidad Aire']=nivelCalidad
    dfPredAEMET['Plus AEMET '+str(dia1F)]=nivelesAEMET1
    dfPredAEMET['Plus AEMET '+str(dia2F)]=nivelesAEMET2
    dfPredAEMET['Plus AEMET '+str(dia3F)]=nivelesAEMET3
    dfPredAEMET['Nivel '+str(dia1F)]=dfPredAEMET['Nivel Base']*(dfPredAEMET['Nivel Base']+dfPredAEMET['Plus Calidad Aire']+dfPredAEMET['Plus AEMET '+str(dia1F)])
    dfPredAEMET['Nivel '+str(dia2F)]=dfPredAEMET['Nivel Base']*(dfPredAEMET['Nivel Base']+dfPredAEMET['Plus Calidad Aire']+dfPredAEMET['Plus AEMET '+str(dia2F)])
    dfPredAEMET['Nivel '+str(dia3F)]=dfPredAEMET['Nivel Base']*(dfPredAEMET['Nivel Base']+dfPredAEMET['Plus Calidad Aire']+dfPredAEMET['Plus AEMET '+str(dia3F)])

    dfPredAEMET
    dfFinal = dfPredAEMET[['Municipio','Codigo','Nivel '+str(dia1F),'Nivel '+str(dia2F),'Nivel '+str(dia3F)]]
    dfFinal
    
    db.PrediccionOTHE.drop()
    recordsdf = json.loads(dfFinal.T.to_json()).values()
    db.PrediccionOTHE.insert_many(recordsdf)
    conexion.close()
	
#Hay que poner 2 horas menos de las que son en realidad debido a problemas en heroku de horas
#scheduler.add_job(timed_job, 'interval', seconds=5)

#realmente se ejecuta a las 08:45
scheduler.add_job(envioMail, 'cron', day_of_week='mon-sun', hour=6, minute=45)

#realmente se ejecuta a las 08:46
scheduler.add_job(actualiza_calidad_aire, 'cron', day_of_week='mon-sun', hour=6, minute=46)

#realmente se ejecuta a las 08:47
scheduler.add_job(prediccionesAEMET, 'cron', day_of_week='mon-sun', hour=6, minute=47)

#realmente se ejecuta a las 08:55
scheduler.add_job(NivelesPolenMadrid, 'cron', day_of_week='mon-sun', hour=6, minute=55)

#realmente se ejecuta a las 09:10
scheduler.add_job(noticias_del_dia, 'cron', day_of_week='mon-sun', hour=7, minute=10)

#realmente se ejecuta a las 09:12
scheduler.add_job(algoritmoPredictivo, 'cron', day_of_week='mon-sun', hour=7, minute=12)
#realmente se ejecuta a las 20:30
#scheduler.add_job(actualiza_calidad_aire, 'cron', day_of_week='mon-sun', hour=18, minute=30)



scheduler.start()
