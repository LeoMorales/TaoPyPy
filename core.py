import xml.etree.ElementTree as ET

from string import Template
from manager import Manager, Tabla, Campo
from utiles import directorioCrear, esDirectorio, archivoCrear, escribirPropiedadArchivoConfiguracion
from constants import CONEXION_TEMPLATE
from constants import DMODELS_ENCABEZADO, DCLASE_TEMPLATE
from constants import MODELS_ENCABEZADO, CLASE_TEMPLATE, ATRIBUTO_TEMPLATE
from constants import MAIN, CONEXION_ACTION, CONEXION_ABM
from constants import GUI_ACTIONS_TEMPLATE, GUI_WIDGET_TEMPLATE, GUI_TEMPLATE_GENERAL
from constants import DB_ENCABEZADO, DB_TABLA_TEMPLATE, DB_MAPPER_BASE, DB_MAPPER_PROPERTIES, DB_FOOTER
from constants import CSS

def parsear_xml(xml_file):
    '''
    Parsea el archivo xml para crear los objetos Campo y Tabla

    @return:
        - manager: Objeto Manager que contiene una coleccion de tablas.
    '''

    #Abrir el xml:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    nombreBD = root.find('meta').find('nombreBD').text
    tipoBD = root.find('meta').find('tipoBD').text
    #new manager
    manager = Manager(nombreBD, tipoBD)

    for tabla in root.findall('tabla'):
        table_name = tabla.get('nombre')
        #new tabla
        new_tabla = Tabla(table_name, [])
        for campo in tabla.findall('campo'):
            campo_nombre = campo.text
            print (table_name, campo_nombre)
            attribs= campo.attrib
            campo_tipo = attribs.get('tipo', None)
            # campo_valor = attribs.get('valor', None)
            campo_es_clave = attribs.get('clave', False)
            campo_es_clave = True if campo_es_clave and campo_es_clave.upper() == 'TRUE' else False
            campo_tamano = attribs.get('tamano', None)
            campo_label = attribs.get('label', campo_nombre.capitalize())#Obtenemos la representacion en el label, si no tiene, es el nombre.
            #new campo
            new_campo = Campo(campo_nombre, campo_tipo, campo_es_clave, campo_tamano, campo_label)
            new_tabla.nuevoCampo(new_campo)

        manager.nuevaTabla(new_tabla)

    print manager.strStatus()
    return manager
    
def crearConexionFile(nombreBD, path_proyecto):
    '''
        Crea el archivo de conexion
    '''

    contenido = CONEXION_TEMPLATE.format(**{'NOMBRE_BASE_DE_DATOS': nombreBD})
    nombre = path_proyecto+'conexion.py'
    archivo_conexion = open(nombre , 'w')
    archivo_conexion.write(contenido)
    archivo_conexion.close()

def crear_dModels(manager, path_proyecto):
    '''
    Crea el archivo dmodels.py.
    Este archivo es el que se debe editar para agregar funcionalidad a los objetos.
    @return:
        - Una lista de todas las clases creadas.

    La lista retornada por este metodo nos va a sevir para crear el models.py luego
    '''

    nombre = path_proyecto+'dmodels.py'
    archivo_dmodels = open(nombre, 'w')
    archivo_dmodels.write(DMODELS_ENCABEZADO)

    nombres_de_clases = [] #nos vamos a guardar los nombres de las clases creadas.
    for tabla in manager.tablas:
        nombre_de_clase = 'd'+tabla.nombre.capitalize()
        nombres_de_clases.append(nombre_de_clase)
        clase_str = DCLASE_TEMPLATE.format(**{'DCLASE_NOMBRE': nombre_de_clase,
                                            'DCLASE_CAMPOS': tabla.str_get_campos(),
                                            'DCLASE_HEADERS': tabla.str_get_encabezados_campos()})
        archivo_dmodels.write(clase_str)

    archivo_dmodels.close()
    return nombres_de_clases

def crear_Models(manager, clases, path_proyecto):
    '''
    Crea el archivo models.py.
    Este archivo es el que contiene las clases de negocio.
    @return:
        - Una lista de todas las clases creadas.

    La lista retornada por este metodo nos va a sevir para crear el models.py luego
    '''

    nombre = path_proyecto+'models.py'
    archivo_models = open(nombre, 'w')
    encabezado = MODELS_ENCABEZADO.format(**{'CLASES_DE_DMODELS': ' ,'.join(clases)})
    archivo_models.write(encabezado)

    for tabla in manager.tablas:
        # print "Analizando...\n", tabla.info()
        data = {
                'CLASE_NOMBRE': tabla.nombre.capitalize(),
                'LISTA_ATRIBUTOS': ' ,'.join([c.get_nombre() for c in tabla.camposSinClave()]),
                'ASIGNACION_ATRIBUTOS': '\n'.join([ATRIBUTO_TEMPLATE.format(**{'ATRIBUTO_NOMBRE':campo.get_nombre()}) for campo in tabla.camposSinClave()])
                }
        clase_str = CLASE_TEMPLATE.format(**data)
        archivo_models.write(clase_str)

    archivo_models.close()
    # return nombres_de_clases

def crear_db_management(manager, path_proyecto):
    '''
    Crea el archivo db_management.py, que se va a encargar luego de crear las tablas de nuestro modelo.
    '''
    data = {
            'MODELOS':manager.nombres_tablas_para_models(),
            'DMODELOS': manager.nombres_tablas_para_dmodels()
            }
    encabezado = DB_ENCABEZADO.format(**data)
    nombre = path_proyecto+'db_management.py'
    archivo_db_management = open(nombre, 'w')
    archivo_db_management.write(encabezado)

    #Por cada tabla, crear las tablas sqlalchemy:
    for tabla in manager.tablas:
        data = {
                'TABLA_NOMBRE': tabla.nombre,
                'COLUMNAS': ",\n".join([campo.representacion_en_columna() for campo in tabla.campos])
        }
        una_tabla = DB_TABLA_TEMPLATE.format(**data)
        archivo_db_management.write(una_tabla)

    for tabla in manager.tablas:
        str_propiedades = ")"
        str_propiedades_d = ")"
        if tabla.tieneForaneas():
            str_propiedades = ', properties={'
            str_propiedades_d = ', properties={'
            for clave_foranea in tabla.clavesForaneas():
                data = {
                        'CAMPO_NOMBRE': clave_foranea.nombre,
                        'OBJ_REFERENCIADO': clave_foranea.nombre.capitalize(),
                        'BACKREF': "%ss"%tabla.nombre
                }
                str_propiedades += DB_MAPPER_PROPERTIES.format(**data)

                #properties_d:
                data['OBJ_REFERENCIADO'] = 'd'+data['OBJ_REFERENCIADO']
                str_propiedades_d += DB_MAPPER_PROPERTIES.format(**data)
            str_propiedades += '})'
            str_propiedades_d += '})'

        str_mapper = DB_MAPPER_BASE.format(**{
                                                'OBJETO':tabla.nombre.capitalize(),
                                                'TABLA': tabla.nombre,
                                                'PROPIEDADES': str_propiedades
            })
        archivo_db_management.write(str_mapper)
        str_mapper = DB_MAPPER_BASE.format(**{
                                                'OBJETO':'d'+tabla.nombre.capitalize(),
                                                'TABLA': tabla.nombre,
                                                'PROPIEDADES': str_propiedades_d
            })
        archivo_db_management.write(str_mapper)


    archivo_db_management.write(DB_FOOTER)
    archivo_db_management.close()

def crear_mainwindow(manager, path_proyecto):
    '''
    Crea nuestro archivo .ui de ventana principal.
    '''
    nombre = path_proyecto+'mainwindow.ui'
    archivo_mainwindow = open(nombre, 'w')

    
    template_action = Template(GUI_ACTIONS_TEMPLATE)
    template_widget = Template(GUI_WIDGET_TEMPLATE)
    template_general = Template(GUI_TEMPLATE_GENERAL)
    str_actions = '' #Se va llenando con los reemplazos de template_action
    str_widgets = '' #Se va llenando con los reemplazos de template_widgets

    for tabla in manager.tablas:
        data = {
            'NOMBRE_CLASE': tabla.nombre.capitalize()
        }
        action_reemplazado = template_action.safe_substitute(data)
        str_actions += "\n"+action_reemplazado
        widget_reemplazado = template_widget.safe_substitute(data)
        str_widgets += '\n'+widget_reemplazado

    data_general = {
        'TITULO_WINDOW': 'Mi Aplicacion',
        'LISTA_WIDGETS': str_widgets,
        'LISTA_ACCIONES': str_actions
    }

    archivo_mainwindow.write(template_general.safe_substitute(data_general))
    archivo_mainwindow.close()


def crearProyecto(nombre, path):
    '''
    Crea el arbol de directorios de nuestro proyecto.
    @params:
        - nombre: Nombre del nuevo proyecto.
        - path: Path del nuevo proyecto.
    '''
    if(path != "" and esDirectorio(path)):
        if(nombre):
            pathCompleto = pathCompletoAux = directorioCrear(path, nombre)

            if not pathCompleto:
                print 'El directorio que se desea crear ya existe.'
                return None

            #Crear los directorios necesarios:
            directorioCrear(pathCompleto, "src")
            archivoCrear(pathCompleto, ".frProject")
            pathCompleto = pathCompleto + "/" + "src"
            directorioCrear(pathCompleto, "forms")
            archivoCrear(pathCompleto+"/"+"forms", "__init__.py")
            directorioCrear(pathCompleto, "images")
            archivoCrear(pathCompleto+"/"+"images", "__init__.py")
            directorioCrear(pathCompleto+"/images", "icons")
            directorioCrear(pathCompleto, "forms_ui")
            archivoCrear(pathCompleto+"/"+"forms_ui", "__init__.py")
            directorioCrear(pathCompleto, "dialogs")
            archivoCrear(pathCompleto+"/"+"dialogs", "__init__.py")
            directorioCrear(pathCompleto, "base_de_datos")
            archivoCrear(pathCompleto+"/"+"base_de_datos", "__init__.py")
            directorioCrear(pathCompleto, "utiles")
            archivoCrear(pathCompleto+"/"+"utiles", "__init__.py")

            #Y guardar el nombre de proyecto:
            escribirPropiedadArchivoConfiguracion("lastProject", pathCompletoAux)
            print "Proyecto creado correctamente."
            return pathCompletoAux
    else:
        print "Debe ingresar un path destino correcto."
        return None

def crear_main(manager, path_proyecto):
    '''
    Crea nuestro archivo main. 
    '''
    nombre = path_proyecto+'main.py'
    archivo_main = open(nombre, 'w')

    template_main = Template(MAIN)
    template_conexion_actions = Template(CONEXION_ACTION)
    template_conexion_abm = Template(CONEXION_ABM)
    str_actions = '' #Se va llenando
    for tabla in manager.tablas:
        for action in ['Alta', 'Baja', 'Modificacion']:
            #Por cada tabla formamos el nombre de la action correspondiente. Por ej: action[Alta|Baja|Modificacion]Producto
            action_name = 'action{}{}'.format(action, tabla.nombre.capitalize())
            if action == 'Alta':
                context = {
                    'ACTION_NOMBRE': action_name,
                    'ACTION': action,
                    'NOMBRE_CLASE': tabla.nombre.capitalize()
                }
                str_actions += '\n'+template_conexion_actions.safe_substitute(context)
            else:
                context = {
                    'ACTION_NOMBRE': action_name,
                    'ACTION': action,
                    'CLASE_ABM': tabla.nombre.capitalize()
                }
                str_actions += '\n'+template_conexion_abm.safe_substitute(context)
        
    relleno_main = {
                    'MODELOS': manager.nombres_tablas_para_models(),
                    'CONEXIONES_ACTIONS': str_actions
    }
    archivo_main.write(template_main.safe_substitute(relleno_main))
    archivo_main.close()

def crear_widgets(manager, path_proyecto):
    '''
    Crea los widgets .ui de la aplicacion.
    '''
    from constants import CENTRAL_WIDGET_ALTA, WIDGET_CAMPO_TEMPLATE, WIDGET_ABM_TEMPLATE
    #Crear widget ABM:
    template_widget_ABM = Template(WIDGET_ABM_TEMPLATE)
    w_nombre = path_proyecto+'widgetABM.ui'
    f = open(w_nombre, 'w')
    f.write(WIDGET_ABM_TEMPLATE)
    f.close()

    #Crear widgets ALTA
    template_central_widget = Template(CENTRAL_WIDGET_ALTA)
    template_campos = Template(WIDGET_CAMPO_TEMPLATE)
    for tabla in manager.tablas:
        str_campos = '' #Se va llenando de campos
        nombre = path_proyecto+'widgetAlta{}.ui'.format(tabla.nombre.capitalize())
        archivo_widget = open(nombre, 'w')
        for i, campo in enumerate(tabla.campos):
            if campo.esClave():
                continue
            info_campo = { #iiija
                'CONTADOR_FILA': i+1,
                'NOMBRE_CAMPO': campo.label,
                'WIDGET_CAMPO': campo.representacion_widget()
            }
            str_campos += '\n'+template_campos.safe_substitute(info_campo)
        
        relleno_main = {
            'CAMPOS_DEL_WIDGET': str_campos,
            'NOMBRE_OBJETO': tabla.nombre.capitalize()
        }
        archivo_widget.write(template_central_widget.safe_substitute(relleno_main))
        archivo_widget.close()

def crear_styless_css(path):
    '''
    Crea un archivo que contiene una constante con los estilos de la aplicacion.
    Para modificar el estilo de nuestra app, se debe modificar esa constante.
    '''
    nombre = path+'styles.py'
    archivo_css = open(nombre, 'w')
    archivo_css.write(CSS)
    archivo_css.close()

def crear_dialogos(manager, path_dialogos):
    '''
    Crea los dialogos de nuestra app. 

    Son los que se van a mostrar al hacer click en algun menu de Admin.
    Una vez creados, se les debe asgregar la funcionalidad necesaria.
    @params:
        - manager: Objeto gestor de todas las tablas.
        - path_dialogos: ruta al directorio en donde se van a crear los dialogos.
    '''
    #crear archivos utiles:
    crear_utiles(path_dialogos)
    from constants import DIALOGOS_MAIN, DIALOGOS_FORANEAS
    template_dialog = Template(DIALOGOS_MAIN)
    template_foraneas = Template(DIALOGOS_FORANEAS)

    for tabla in manager.tablas:
        nombre = path_dialogos+'widgetAlta{}.py'.format(tabla.nombre.capitalize())
        archivo_dialogo = open(nombre, 'w')
        str_foraneas = ""
        for campo in tabla.clavesForaneas():
            contexto_campo = {
                'NOMBRE_CAMPO': campo.nombre,
                'NOMBRE_OBJETO': campo.nombre.capitalize()
            }
            str_foraneas += template_foraneas.safe_substitute(contexto_campo)

        str_obtencion_de_datos = ""
        for campo in tabla.campos:
            if campo.esClave():
                continue
            str_obtencion_de_datos += "\n        "+campo.representacion_obtencion_dialogo()
        
        str_obtencion_de_datos += '\n        nuevo = {TABLA_NOMBRE}({LISTA_ATRIBUTOS})'.format(**{
                'TABLA_NOMBRE': tabla.nombre.capitalize(),
                'LISTA_ATRIBUTOS': tabla.campos_para_creacion()
            })
        str_obtencion_de_datos += '\n        self.session.add(nuevo)'
        # str_obtencion_de_datos += '\n        print "CREADO: ", str(nuevo)'

        relleno = {#o contexto...
            'NOMBRE_OBJETO': tabla.nombre.capitalize(),
            'MODELOS': manager.nombres_tablas_para_models(),
            'FORANEAS': str_foraneas,
            'OBTENCION_DE_DATOS': str_obtencion_de_datos
        }
        archivo_dialogo.write(template_dialog.safe_substitute(relleno))
        archivo_dialogo.close()


def crear_utiles(path):
    from constants import MODELO_TABLA_UTILES, CENTRAL_WIDGET_ABM
    f = open(path+'ModeloTabla.py', 'w')
    f.write(MODELO_TABLA_UTILES)
    f.close()

    f = open(path+'widgetABM.py', 'w') #Generico...
    f.write(CENTRAL_WIDGET_ABM)
    f.close()
