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


#scheduler.add_job(timed_job, 'interval', seconds=5)
scheduler.add_job(envioMail, 'cron', day_of_week='mon-fri', hour=20, minute=02)

scheduler.start()


