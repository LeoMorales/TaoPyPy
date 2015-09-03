import os
from argparse import ArgumentParser
from core import parsear_xml, crearConexionFile, crear_dModels, crear_Models, crear_db_management, crear_mainwindow, crearProyecto, crear_main, crear_widgets, crear_styless_css, crear_dialogos
def main(project_name, path, xml_file):
    import sys
    #Crear arbol de directorios:
    path_completo = crearProyecto(project_name, path)
    if not path_completo:
        sys.exit()
    #MAIN:
    manager = parsear_xml(xml_file)

    # path_base = path_completo
    print 'PATH: ', path_completo
    path_proyecto = path_completo+'/src/base_de_datos/'
    #Crear el archivo conexion:
    crearConexionFile(manager.nombreBD, path_proyecto)
    #Crear Models y dModels:
    clases_dmodels = crear_dModels(manager, path_proyecto)
    print "Creadas: ",  clases_dmodels
    crear_Models(manager, clases_dmodels, path_proyecto)
    #Crear el db manager:
    crear_db_management(manager, path_proyecto)
    #Crear GUI basica
    path_proyecto = path_completo+'/src/forms_ui/'
    crear_mainwindow(manager, path_proyecto)
    crear_widgets(manager, path_proyecto)

    #crear forms (compilar):
    command = "pyuic4 -x {} -o {}".format(path_proyecto + 'mainwindow.ui', path_completo+'/src/forms/mainwindow.py')
    print 'EJECUTANDO: ', command
    os.system(command)
    for tabla in manager.tablas:
        command = "pyuic4 -x {} -o {}".format(path_proyecto + 'widgetAlta{}.ui'.format(tabla.nombre.capitalize()),
                                            path_completo+'/src/forms/c_widgetAlta{}.py'.format(tabla.nombre.capitalize()))
        print 'EJECUTANDO: ', command
        os.system(command)

    command = "pyuic4 -x {} -o {}".format(path_proyecto + 'widgetABM.ui',
                                        path_completo+'/src/forms/c_widgetABM.py')
    print 'EJECUTANDO: ', command
    os.system(command)

    #Crear dialogos (widgets que usan los widgets compilados y le agregan funcionalidad)
    path_proyecto = path_completo+'/src/dialogs/'
    crear_dialogos(manager, path_proyecto)
    #Crear un main
    path_proyecto = path_completo+'/src/'
    crear_main(manager, path_proyecto)

    #crear archivo css
    crear_styless_css(path_proyecto)


if __name__ == '__main__':
    parser = ArgumentParser(description='===== TaoPyPy =====')
    parser.add_argument('--new', metavar='N', type=str, nargs='?',
                       help='Crea un nuevo proyecto')
    parser.add_argument('--path', metavar='P', type=str, nargs='?',
                       help='Path en donde se crea el nuevo proyecto')
    parser.add_argument('--dataModelSource', metavar='D', type=str, nargs='?',
                       help='Archivo xml en el cual se encuentra la definicion del modelo de datos')
    args = parser.parse_args()
    
    data_xml = 'data.xml'
    if args.dataModelSource:
        data_xml = args.dataModelSource
    if args.new:
        path_proyecto = './Proyectos/' if not args.path else args.path
        main(args.new, path_proyecto, data_xml)