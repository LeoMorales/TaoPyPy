import os
import xml.etree.ElementTree as ET

def esDirectorio(path):
    return os.path.isdir(path)

def esArchivo(path):
    return os.path.isfile(path)

def directorioCrear(path, nombre):
    '''
    Crea el directorio y retorna el path de dicho directorio
    '''
    directorio = os.path.join(path, nombre)
    if not os.path.isdir(directorio):
        os.mkdir(directorio)
        print 'Creado:\t', directorio, '...'
        return directorio
    else:
        return None

def archivoCrear(path, nombre):
    archi=open(path+"/"+nombre,'w')
    archi.close()      

def archExiste(archivo):
    return os.path.exists(archivo)

def escribirPropiedadArchivoConfiguracion(propiedad, valor):
    if(archExiste("config.xml")):
        tree = ET.parse('config.xml')
        root = tree.getroot()
        a_cambiar = root.find(propiedad)
        a_cambiar.text = str(valor)
        a_cambiar.set('updated', 'yes')
        tree.write('config.xml')

def leerConfiguracion(campo):
    if(archExiste("config.xml")):
        print "-- leyendo config --"
        tree = ET.parse('config.xml')
        root = tree.getroot()
        return root.find(campo).text

def leerPropiedadDeXML(campo, nombre_del_xml):
    if(archExiste(nombre_del_xml)):
        print "-- leyendo config --"
        tree = ET.parse(nombre_del_xml)
        root = tree.getroot()
        return root.find(campo).text
    else:
        print 'El archivo xml no existe.'

        