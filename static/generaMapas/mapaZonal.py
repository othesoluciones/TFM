
import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def dibujaMunicipiosErrores(first,micolor,finrango1, finrango2, fin, ax):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.path import Path
    import matplotlib.patches as patches
    dibuja= True
    if micolor==1:
        micolor2='maroon'
    elif (micolor==2): 
        micolor2='olive'
    elif (micolor==3):
        micolor2='orangered'
    elif (micolor==4):
        micolor2='skyblue'
    elif (micolor==5):
        micolor2='gold'
    elif (micolor==6):
        micolor2='Crimson'
    else:
        micolor2='DarkKhaki'
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
    if micolor==1:
        micolor2='maroon'
    elif (micolor==2): 
        micolor2='olive'
    elif (micolor==3):
        micolor2='orangered'
    elif (micolor==4):
        micolor2='skyblue'
    elif (micolor==5):
        micolor2='gold'
    elif (micolor==6):
        micolor2='Crimson'
    else:
        micolor2='DarkKhaki'
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


def dibuja_mapa_zonal():
    import datetime
    import shapefile
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.path import Path
    import matplotlib.patches as patches
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
    #Dibujamos el mapa de Madrid en 7 colores en funcion de la zona en la que se encuentra
    from lxml import etree
    doc=etree.parse("../Municipios/madrid.xml")
    muni=doc.findall("municipio")
    sf = shapefile.Reader("../Municipios/200001493.shp")
    shapes =sf.shapeRecords()

    fig = plt.figure(figsize=(11,11))
    ax = fig.add_subplot(111)


    for shape in sf.shapeRecords():
        nombreMunicipio = elimina_tildes((shape.record[2]).decode('windows-1252'))
        nombreMunicipioShape=nombreMunicipio
        #print nombreMunicipio
        i=0
        encontrado=False
        while(i<len(muni) and encontrado==False):
            if(elimina_tildes(unicode(muni[i].text.upper()))==nombreMunicipioShape.upper()):
                encontrado=True
                color =muni[i].attrib['zona']
                print nombreMunicipio, " -->", color 
            else:
                i=i+1  
        if (nombreMunicipio in diccionarioMunicipiosErroneos):
            finrango1= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango1']
            finrango2= diccionarioMunicipiosErroneos[nombreMunicipio]['finrango2']
            dibujaMunicipiosErrores(shape,int(color),finrango1,finrango2,len(shape.shape.points), ax)
        else:
            dibujaMunicipios(shape,int(color), ax)



    ax.autoscale_view()

    nomFich = "dirTempGeneraMapas/COLOR.png"


    plt.axis('off')
    plt.savefig(nomFich, bbox_inches='tight')
    plt.close(fig)


def dibujaLeyenda():
    import matplotlib.patches as patches
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(11,11))
    ax = fig.add_subplot(111)
    maroon_patch = patches.Patch(color='maroon', label='Madrid Capital')
    olive_patch = patches.Patch(color='olive', label='Corredor del Henares')
    orangered_patch = patches.Patch(color='orangered', label='Zona Sur')
    skyblue_patch = patches.Patch(color='skyblue', label='Zona Noroeste')
    gold_patch = patches.Patch(color='gold', label='Zona Sierra Norte')
    crimson_patch = patches.Patch(color='crimson', label='Cuenca del Alberche')
    tajuna='Cuenca del Taju\xc3\xb1a'
    darkkhaki_patch = patches.Patch(color='DarkKhaki', label=tajuna.decode('utf-8'))
    plt.legend(handles=[maroon_patch,olive_patch, orangered_patch, skyblue_patch,gold_patch, crimson_patch,darkkhaki_patch ], fontsize=29, loc='center left')
    nomFich = "dirTempGeneraMapas/Leyenda.png"


    plt.axis('off')
    plt.savefig(nomFich, bbox_inches='tight')
    plt.close(fig)