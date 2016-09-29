#Conectamos a la base de datos
import base64
import json
from pymongo import MongoClient as Connection

cadenaCon= 'mongodb://othesoluciones:'+base64.b64decode("b3RoZXNvbHVjaW9uZXM=")+'@ds029635.mlab.com:29635/othesoluciones1'
MONGODB_URI =cadenaCon
conexion = Connection(MONGODB_URI)
db = conexion.othesoluciones1

import pandas as pd

#Calendario polinico (http://encuentralainspiracion.es/la-alergia-respiratoria/tipos-de-alergenos/alergia-al-polen/calendario-de-polinizacion/)
columnas =['Mes','Nivel']
datos = [(1,0),(2,0),(3,1),(4,2),(5,2),(6,2),(7,1),(8,0),(9,0),(10,0),(11,0),(12,0)]

df=pd.DataFrame(datos,columns=columnas)

recordsdf = json.loads(df.T.to_json()).values()
db.calendarioPolen.insert_many(recordsdf)
conexion.close()