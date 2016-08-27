import os
import time
import base64
import smtplib
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig()

scheduler = BlockingScheduler()
def envioMail():

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
 #MONGODB_URI = 'mongodb://othesoluciones:othesoluciones@ds029635.mlab.com:29635/othesoluciones1'
# db = Connection(MONGODB_URI).othesoluciones1 
 conexion = Connection(MONGODB_URI)
 db = conexion.othesoluciones1

 print type(db)
 #calidadAire = {}
 primeraVez = True

 #for i in range (2,8):
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
        columnas.append(metricas[k].strong.a['title'])
    
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
    
    df.rename(columns=lambda x: x.replace('.', ''), inplace=True)
    df.columns
    
    recordsdf = json.loads(df.T.to_json()).values()
    db.calidad_aire_23082016_I.insert_many(recordsdf)
    
    dfFinal = df.set_index('Estacion')
    
    

    dfFinal['Dia']=dia
    dfFinal['Hora']=hora
 conexion.close() 

#Hay que poner 2 horas menos de las que son en realidad debido a problemas en heroku de horas
#scheduler.add_job(timed_job, 'interval', seconds=5)
#realmente se ejecuta a las 13:42
scheduler.add_job(envioMail, 'cron', day_of_week='mon-sun', hour=12, minute=10)


#realmente se ejecuta a las 13:42
scheduler.add_job(actualiza_calidad_aire, 'cron', day_of_week='mon-sun', hour=11, minute=50)
#realmente se ejecuta a las 22:35
scheduler.add_job(actualiza_calidad_aire, 'cron', day_of_week='mon-sun', hour=20, minute=35)
scheduler.start()


