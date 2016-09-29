import shapefile
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))



def dibujaMunicipiosErroresROJO(first,micolor,finrango1, finrango2, fin, ax):
    dibuja= True
    if micolor==1:
      micolor2='red'
      milw=2
    else: 
       micolor2='grey'
       milw=1
    
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
         patch = patches.PathPatch(path, facecolor=micolor2, lw=milw)
         ax.add_patch(patch)
		 
def dibujaMunicipiosROJO(first,micolor, ax):
    if micolor==1:
      micolor2='red'
      milw=2
    else: 
       micolor2='grey'
       milw=1
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
    patch = patches.PathPatch(path, facecolor=micolor2, lw=milw)
    ax.add_patch(patch)

	
def dibujaMapasNivelAlto():	
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
	#Leemos el xml
	from lxml import etree
	import time
	doc=etree.parse("../Municipios/madrid.xml")
	muni=doc.findall("municipio")

	#Ejecutado para generar las imagenes de los municipios
	sf = shapefile.Reader("../Municipios/200001493.shp")
	shape =sf.shapeRecords()
	for alfab in range(0,len(shape)):
	 #Dibujamos un solo municipio de forma aleatoria. Coloreado de rojo
	 # Y lo guardamos en un png sin mostrar ejes ni espacioes en blanco
	 
	 fig = plt.figure(figsize=(11,11))
	 ax = fig.add_subplot(111)
	 shape =sf.shapeRecords()
	 nombreMunicipio = elimina_tildes((shape[alfab].record[2]).decode('windows-1252'))
	 #print nombreMunicipio
	 if (nombreMunicipio in diccionarioMunicipiosErroneos):
		finrango1= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango1']
		finrango2= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango2']
		dibujaMunicipiosErroresROJO(shape[alfab],1,finrango1,finrango2,len(shape[alfab].shape.points), ax)
	 else:
		dibujaMunicipiosROJO(shape[alfab],1, ax)
	 ax.autoscale_view()
	 nombreMunicipioShape=nombreMunicipio
	 i=0
	 encontrado=False
	 while(i<len(muni) and encontrado==False):
			if(elimina_tildes(unicode(muni[i].text.upper()))==nombreMunicipioShape.upper()):
				encontrado=True
				nombreMunicipio=elimina_tildes(unicode(muni[i].text))
				print nombreMunicipio
			else:
				i=i+1    
	 nomFich = "dirTempGeneraMapas/"+nombreMunicipio+"-Alto.png"
	 plt.axis('off')

	 plt.savefig(nomFich, bbox_inches='tight')
	 plt.close(fig)


	#import time
	#time.sleep(60)

	#Dibujamos el mapa de Madrid en gris a excepcion de 
	# un municipio elegido de forma alfabetica que se coloreara de rojo
	sf = shapefile.Reader("../Municipios/200001493.shp")
	shapes =sf.shapeRecords()
	for alfab in range(0,len(shapes)):
	 fig = plt.figure(figsize=(11,11))
	 ax = fig.add_subplot(111)


	 for shape in sf.shapeRecords():
		nombreMunicipio = elimina_tildes((shape.record[2]).decode('windows-1252'))
		if (nombreMunicipio in diccionarioMunicipiosErroneos):
			finrango1= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango1']
			finrango2= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango2']
			dibujaMunicipiosErroresROJO(shape,0,finrango1,finrango2,len(shape.shape.points), ax)
		else:
			dibujaMunicipiosROJO(shape,0, ax)
	 

	#PARTE DE DIBUJO DE UN MUNICIPIO EN ROJO
	 nombreMunicipio = elimina_tildes((shapes[alfab].record[2]).decode('windows-1252'))
	 if (nombreMunicipio in diccionarioMunicipiosErroneos):
		finrango1= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango1']
		finrango2= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango2']
		dibujaMunicipiosErroresROJO(shapes[alfab],1,finrango1,finrango2,len(shapes[alfab].shape.points), ax)
	 else:
		dibujaMunicipiosROJO(shapes[alfab],1, ax)


		
	 ax.autoscale_view()
	 nombreMunicipioShape=nombreMunicipio
	 i=0
	 encontrado=False
	 while(i<len(muni) and encontrado==False):
			if(elimina_tildes(unicode(muni[i].text.upper()))==nombreMunicipioShape.upper()):
				encontrado=True
				nombreMunicipio=elimina_tildes(unicode(muni[i].text))
				print nombreMunicipio
			else:
				i=i+1  
	 nomFich = "dirTempGeneraMapas/"+nombreMunicipio+"-CAM-Alto.png"
	 plt.axis('off')
	 plt.savefig(nomFich, bbox_inches='tight')
	 plt.close(fig)

