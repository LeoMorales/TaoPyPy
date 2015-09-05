#=======================================================#
# Constates archivo conexion.py:
#=======================================================#
CONEXION_TEMPLATE = """
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class Conexion():

    def __init__(self, nombre_db='{NOMBRE_BASE_DE_DATOS}.db'):
        enginame = 'sqlite:///'+nombre_db
        self.my_db = create_engine(enginame)
        self.metadata  = MetaData(self.my_db)
        

    def crearSession(self):
        Session = sessionmaker(bind=self.my_db)
        session = Session()
        return session      

    @staticmethod
    def getSession():
        return Conexion.singleSession

    @staticmethod
    def setSession(session):
        Conexion.singleSession = session

    def crearTablas(self):
        self.metadata.create_all(self.my_db)

"""

#=======================================================#
# Constates archivo dmodels.py:
#=======================================================#
DMODELS_ENCABEZADO = """
'''
Extiende la funcionalidad de las clases del Modelo.
'''
from conexion import Conexion
"""

DCLASE_TEMPLATE = """
class {DCLASE_NOMBRE}(object):
    '''docstring for {DCLASE_NOMBRE}'''

    def getId(self):
        return self.id

    def __str__(self):
        return '{DCLASE_NOMBRE} #%s'%(self.getId())

    def valores_de_campos(self):
        '''
        Retorna los campos que se van a mostrar en la tabla de listado (ABM).
        Si se modifican los campos devueltos, recordar modificar el correspondiente en nombres_de_campos
        '''
        return [ {DCLASE_CAMPOS} ]

    def nombres_de_campos(self):
        '''
        Representacion de los campos
        '''
        return [ {DCLASE_HEADERS} ]

"""

#=======================================================#
# Constates archivo models.py:
#=======================================================#
MODELS_ENCABEZADO = """
'''
Modelos. Clases de negocio.
like django style.
'''
from dmodels import {CLASES_DE_DMODELS} #ejemplo: dUser, dAdress, dProducto, dCategoria, dRetiro, dIngreso
"""

CLASE_TEMPLATE = """
class {CLASE_NOMBRE}(d{CLASE_NOMBRE}):
    def __init__(self, {LISTA_ATRIBUTOS}):
{ASIGNACION_ATRIBUTOS}

    @staticmethod
    def buscarTodos(session):
        renglones = session.query({CLASE_NOMBRE}).all()
        return renglones

    @staticmethod
    def buscarPorID(session,id{CLASE_NOMBRE}):
        renglones = session.query({CLASE_NOMBRE}).filter({CLASE_NOMBRE}.id==id{CLASE_NOMBRE})
        return renglones.first()

"""

# ATRIBUTO_TEMPLATE = """
#         self.{ATRIBUTO_NOMBRE} = {ATRIBUTO_NOMBRE}
# """

ATRIBUTO_TEMPLATE = "        self.{ATRIBUTO_NOMBRE} = {ATRIBUTO_NOMBRE}"

#=======================================================#
# Constates archivo db_management.py:
#=======================================================#
DB_ENCABEZADO = """
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import mapper, relationship
from conexion import Conexion
from models import {MODELOS}#Ej: Adress, User, Producto, Categoria, Retiro, Ingreso
from dmodels import {DMODELOS}#Ej: dAdress, dUser, dProducto, dCategoria, dRetiro, dIngreso

def crear_esquema():
    '''
    Crea el esquema de Base de Datos, mappea las tablas con las clases correspondientes
    @return:
        - conexion.
    '''
    bd = Conexion()
    metadata = bd.metadata

    session = bd.crearSession()
    bd.setSession(session)

    #TABLAS:
"""

DB_TABLA_TEMPLATE = """
    {TABLA_NOMBRE} = Table('{TABLA_NOMBRE}', metadata,
{COLUMNAS}
            )
"""

DB_MAPPER_BASE = """
    mapper({OBJETO}, {TABLA}{PROPIEDADES}
"""

DB_MAPPER_PROPERTIES = """'{CAMPO_NOMBRE}' : relationship({OBJ_REFERENCIADO}, backref='{BACKREF}'),"""

DB_FOOTER = """
    bd.crearTablas()
    print "BASE DE DATOS CREADA CON EXITO"
    return bd
"""

#=======================================================#
# Constates archivo main_window.ui:
#=======================================================#

GUI_WIDGET_TEMPLATE = """
            <widget class="QMenu" name="menu${NOMBRE_CLASE}">
                <property name="title">
                    <string>$NOMBRE_CLASE</string>
                </property>
                
                <addaction name="actionAlta${NOMBRE_CLASE}"/>
                <addaction name="actionBaja${NOMBRE_CLASE}"/>
                <addaction name="actionModificacion${NOMBRE_CLASE}"/>
            </widget>
            <addaction name="menu${NOMBRE_CLASE}"/>
"""

GUI_ACTIONS_TEMPLATE = """
    <action name="actionAlta${NOMBRE_CLASE}">
       <property name="text">
        <string>Alta $NOMBRE_CLASE</string>
       </property>
    </action>
    <action name="actionBaja${NOMBRE_CLASE}">
       <property name="text">
        <string>Baja $NOMBRE_CLASE</string>
       </property>
    </action>
    <action name="actionModificacion${NOMBRE_CLASE}">
       <property name="text">
        <string>Modificacion $NOMBRE_CLASE</string>
       </property>
    </action>
"""

GUI_TEMPLATE_GENERAL = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
<class>MainWindow</class>
<widget class="QMainWindow" name="MainWindow">
    <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>800</width>
        <height>600</height>
       </rect>
    </property>
    <property name="windowTitle">
       <string>$TITULO_WINDOW</string>
    </property>
    <widget class="QWidget" name="centralwidget"/>
    <widget class="QMenuBar" name="menubar">
        <property name="geometry">
            <rect>
             <x>0</x>
             <y>0</y>
             <width>800</width>
             <height>21</height>
            </rect>
        </property>
        <widget class="QMenu" name="menuArchivo">
            <property name="title">
                <string>A&amp;rchivo</string>
            </property>
            <addaction name="actionSalir"/>
        </widget>
        <widget class="QMenu" name="menuAdmin">
            <property name="title">
                <string>&amp;Admin</string>
            </property>

            <!-- BUCLE: UN MENU POR CADA CLASE:  -->

$LISTA_WIDGETS        
            <!-- FIN NUEVO -->
        </widget>
        <addaction name="menuArchivo"/>
        <addaction name="menuAdmin"/>
    </widget>
    <widget class="QStatusBar" name="statusbar"/>
    <widget class="QToolBar" name="toolBar">
       <property name="windowTitle">
        <string>toolBar</string>
       </property>
       <attribute name="toolBarArea">
        <enum>TopToolBarArea</enum>
       </attribute>
       <attribute name="toolBarBreak">
        <bool>false</bool>
       </attribute>
    </widget>
    <widget class="QToolBar" name="toolBar_2">
       <property name="windowTitle">
        <string>toolBar_2</string>
       </property>
       <attribute name="toolBarArea">
        <enum>TopToolBarArea</enum>
       </attribute>
       <attribute name="toolBarBreak">
        <bool>false</bool>
       </attribute>
       <!-- ACCIONES DE LA BARRA DE TAREAS: -->

    </widget>
    <!-- DEFINICION DE LAS ACCIONES -->
    <action name="actionSalir">
        <property name="text">
            <string>Salir</string>
        </property>
        <property name="shortcut">
            <string>Ctrl+Q</string>
        </property>
    </action>
$LISTA_ACCIONES
    <!-- FIN DEFINICION DE LAS ACCIONES -->
 </widget>

<connections/>
</ui>
"""

#=======================================================#
# Constates archivo main_window.ui:
#=======================================================#

MAIN = """import sys
from PyQt4 import QtGui, QtCore
from forms.mainwindow import Ui_MainWindow
from styles import STYLES
from base_de_datos.db_management import crear_esquema
from base_de_datos.models import $MODELOS #Ejemplo: Categoria, Producto
from base_de_datos.conexion import Conexion

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(STYLES)
        self.bd = crear_esquema()
        self.session = Conexion.getSession()        

    @QtCore.pyqtSlot()
    def on_actionSalir_triggered(self):
        '''
        Codigo click actionSalir
        '''
        print "Click en accion actionSalir"

    $CONEXIONES_ACTIONS

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
"""

CONEXION_ACTION = """
    @QtCore.pyqtSlot()
    def on_${ACTION_NOMBRE}_triggered(self):
        '''
        Codigo click $ACTION
        '''
        print "Click en accion $ACTION_NOMBRE"
        from dialogs.widget${ACTION}${NOMBRE_CLASE} import Form${ACTION}${NOMBRE_CLASE}
        widget = Form${ACTION}${NOMBRE_CLASE}(self)
        self.setCentralWidget(widget)

"""
CONEXION_ABM = """
    @QtCore.pyqtSlot()
    def on_${ACTION_NOMBRE}_triggered(self):
        '''
        Codigo click $ACTION
        '''
        print "Click en accion $ACTION_NOMBRE"
        from dialogs.widgetABM import FormABM
        widget = FormABM(self, $CLASE_ABM, self.on_baja${CLASE_ABM}_callback, self.on_modificar${CLASE_ABM}_callback, self.on_nuevo${CLASE_ABM}_callback)
        self.setCentralWidget(widget)

"""

MAIN_CALLBACKS_TEMPLATE = """
    def on_baja${TABLA_NOMBRE}_callback(self, elemento):
        print '#'*20
        print 'BAJA: ', elemento.nombre
        print '#'*20
        respuesta = QtGui.QMessageBox.warning(self,'Baja',
                                "El elemento va a ser eliminado de forma permanente. Desea continuar?",
                                QtGui.QMessageBox.Ok,
                                QtGui.QMessageBox.Cancel)

        if respuesta == QtGui.QMessageBox.Ok:
            print 'ELIMINAR!'
            self.session.delete(elemento)
            self.session.commit()
        elif respuesta == QtGui.QMessageBox.Cancel:
            print 'CANCELAR!'


    def on_modificar${TABLA_NOMBRE}_callback(self, elemento):
        print '#'*20
        print 'Modificar: ', elemento.nombre
        print '#'*20
        from dialogs.widgetAlta${TABLA_NOMBRE} import FormAlta${TABLA_NOMBRE}
        widget = FormAlta${TABLA_NOMBRE}(self, elemento)
        self.setCentralWidget(widget)        

    def on_nuevo${TABLA_NOMBRE}_callback(self, elemento):
        print '#'*20
        print 'NUEVO: ', elemento.nombre
        print '#'*20
        self.on_actionAlta${TABLA_NOMBRE}_triggered()

"""


#=======================================================#
# Constates archivo styles:
#=======================================================#

CSS = """STYLES = '''
QMainWindow{
    background-color: #97282C; /*bordo*/
}

QGroupBox{
    font: 75 12pt "Calibri";
    border: none;
    background-color: #428F89; /*azul verdoso*/
    border-radius: 5px;
    color:#AB3334;
}
QPushButton{
    background-color: #3D3C3A;
    border: 2px solid #B08B0D; /*mostaza*/
    border-radius: 6px;
    padding: 5px;
    color: #B08B0D; /*mostaza*/
}
QLabel{
    background-color: #428F89; /*azul verdoso*/
    border-radius: 6px;
    padding: 5px;
    color: #C7D0D5; /*mostaza*/
    text-transform: uppercase;
    font-weight: 700;
}

QLineEdit, QSpinBox, QComboBox{
    background-color:#F5EACD;
}
#labelTitulo{
    background-color: black;
    color: white;
}
#labelTitulo:hover
{
    border: 1px solid #B08B0D; /*mostaza*/
    background-color: white;
    color: black;
}
'''
"""

#=======================================================#
# Constates archivo widget[X][Tabla].ui:
# X = [Alta, Baja, Modificacion]
#=======================================================#
CENTRAL_WIDGET_ALTA = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>FormAlta${NOMBRE_OBJETO}</class>
 <widget class="QWidget" name="Form${NOMBRE_OBJETO}">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Alta ${NOMBRE_OBJETO}</string>
  </property>
  <property name="styleSheet">
   <string notr="true"/>
  </property>
  <layout class="QHBoxLayout" name="horizontalLayout_2">
   <item>
    <spacer name="horizontalSpacer_2">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>40</width>
       <height>20</height>
      </size>
     </property>
    </spacer>
   </item>
   <item>
    <layout class="QVBoxLayout" name="verticalLayout_2">
     <item>
      <spacer name="verticalSpacer">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
       <property name="sizeHint" stdset="0">
        <size>
         <width>20</width>
         <height>40</height>
        </size>
       </property>
      </spacer>
     </item>
     <item>
      <widget class="QGroupBox" name="groupBox">
       <property name="title">
        <string/>
       </property>
       <layout class="QVBoxLayout" name="verticalLayout">
        <item>
         <widget class="QLabel" name="labelTitulo">
          <property name="text">
           <string>Alta $NOMBRE_OBJETO</string>
          </property>
         </widget>
        </item>
        <item>
         <layout class="QFormLayout" name="formLayout">
          <property name="labelAlignment">
           <set>Qt::AlignRight|Qt::AlignTrailing|Qt::AlignVCenter</set>
          </property>
          <property name="formAlignment">
           <set>Qt::AlignLeading|Qt::AlignLeft|Qt::AlignTop</set>
          </property>
          <!-- Comienzo items (campos del objeto/tabla) -->
          $CAMPOS_DEL_WIDGET
          <!-- FIN items -->
         </layout>
        </item>
        <item>
         <layout class="QHBoxLayout" name="horizontalLayout">
          <property name="spacing">
           <number>4</number>
          </property>
          <property name="topMargin">
           <number>0</number>
          </property>
          <item>
           <spacer name="horizontalSpacer">
            <property name="orientation">
             <enum>Qt::Horizontal</enum>
            </property>
            <property name="sizeHint" stdset="0">
             <size>
              <width>40</width>
              <height>20</height>
             </size>
            </property>
           </spacer>
          </item>
          <item>
           <widget class="QPushButton" name="pushButtonOk">
            <property name="text">
             <string>Ok</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="pushButtonCancelar">
            <property name="text">
             <string>Cancelar</string>
            </property>
           </widget>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
     </item>
     <item>
      <spacer name="verticalSpacer_2">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
       <property name="sizeHint" stdset="0">
        <size>
         <width>20</width>
         <height>40</height>
        </size>
       </property>
      </spacer>
     </item>
    </layout>
   </item>
   <item>
    <spacer name="horizontalSpacer_3">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>40</width>
       <height>20</height>
      </size>
     </property>
    </spacer>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>

"""

#ejemplo de CAMPOS_DEL_WIDGET
          # <!-- * Labels columna izquierda -->
          # <item row="1" column="0">
          #  <widget class="QLabel" name="label">
          #   <property name="text">
          #    <string>Nombre:</string>
          #   </property>
          #  </widget>
          # </item>
          # <!-- * Campos columna derecha -->
          # <item row="1" column="1">
          #  <widget class="QLineEdit" name="lineEditNombre"/>
          # </item>
          # <item row="2" column="0">
          #  <widget class="QLabel" name="label_2">
          #   <property name="text">
          #    <string>Descripcion:</string>
          #   </property>
          #  </widget>
          # </item>
          # <item row="2" column="1">
          #  <widget class="QLineEdit" name="lineEditDescripcion"/>
          # </item>
          # <item row="3" column="0">
          #  <widget class="QLabel" name="label_3">
          #   <property name="text">
          #    <string>Stock:</string>
          #   </property>
          #  </widget>
          # </item>
          # <item row="3" column="1">
          #  <widget class="QSpinBox" name="spinBoxStock"/>
          # </item>
          # <item row="4" column="0">
          #  <widget class="QLabel" name="label_4">
          #   <property name="text">
          #    <string>Cantidad Minima:</string>
          #   </property>
          #  </widget>
          # </item>
          # <item row="4" column="1">
          #  <widget class="QSpinBox" name="spinBoxCantidadMinima"/>
          # </item>
          # <item row="5" column="0">
          #  <widget class="QLabel" name="label_5">
          #   <property name="text">
          #    <string>Tiempo de Reposicion:</string>
          #   </property>
          #  </widget>
          # </item>
          # <item row="5" column="1">
          #  <widget class="QSpinBox" name="spinBoxTiempoReposicion"/>
          # </item>
          # <item row="6" column="0">
          #  <widget class="QLabel" name="label_6">
          #   <property name="text">
          #    <string>Categoria:</string>
          #   </property>
          #  </widget>
          # </item>
          # <item row="6" column="1">
          #  <widget class="QComboBox" name="comboBoxCategorias"/>
          # </item>

WIDGET_CAMPO_TEMPLATE = """
          <!-- * Labels columna izquierda -->
          <item row="${CONTADOR_FILA}" column="0">
           <widget class="QLabel" name="label">
            <property name="text">
             <string>${NOMBRE_CAMPO}:</string>
            </property>
           </widget>
          </item>
          <!-- * Campos columna derecha -->
          <item row="${CONTADOR_FILA}" column="1">
            <!-- WIDGET ejemplo: <widget class="QLineEdit" name="lineEditNombre"/> -->
            $WIDGET_CAMPO
          </item>
"""

#=======================================================#
# Constantes dialogos
#=======================================================#

DIALOGOS_MAIN = """import sys
sys.path.append('..')
from forms.c_widgetAlta${NOMBRE_OBJETO} import Ui_FormAlta${NOMBRE_OBJETO}
from PyQt4 import QtCore, QtGui

from base_de_datos.conexion import Conexion
#Manejo de objetos:
from base_de_datos.models import $MODELOS #Por ejemplo: Categoria, Producto

class FormAlta${NOMBRE_OBJETO}(QtGui.QWidget):
    '''Agregar la funcionalidad del widget'''
    def __init__(self, parent, elemento_a_modificar=None):
        super(FormAlta${NOMBRE_OBJETO}, self).__init__(parent)
        self.parent = parent
        self.ui = Ui_FormAlta${NOMBRE_OBJETO}()
        self.ui.setupUi(self)

        self.session = Conexion.getSession()
        #Si tiene foraneas cargar los combos correspondientes:
  
$FORANEAS 

        if elemento_a_modificar:
            self.ui.labelTitulo.setText(QtCore.QString('Modificacion ${NOMBRE_OBJETO}:'))
            self.elemento_a_modificar = elemento_a_modificar
            self.ui.pushButtonOk.clicked.connect(self.modificacion)
            self.setup_para_modificar()
        else:
            self.ui.pushButtonOk.clicked.connect(self.alta)

    def get_clave_del_elemento(self, id_elemento_buscado, diccionario):
        for index, id_elemento in diccionario.iteritems():
            if id_elemento == id_elemento_buscado:
                return index

    def alta(self):
        $OBTENCION_DE_DATOS
        self.session.commit()
        QtGui.QMessageBox.information(self,"Alta","Alta registrada con exito!")
        print "CREADO: ", str(nuevo)
        self.hide()

    def setup_para_modificar(self):
        # self.ui.lineEditNombre.setText(QtCore.QString("%s"%self.elemento_a_modificar.nombre))
        # self.ui.lineEditDescripcion.setText(QtCore.QString("%s"%self.elemento_a_modificar.descripcion))
        $SETUP_DE_DATOS


    def modificacion(self):
        # self.elemento_a_modificar.nombre = str(self.ui.lineEditNombre.text())
        # self.elemento_a_modificar.descripcion = str(self.ui.lineEditDescripcion.text())
        $DATOS_PARA_MODIFICAR
        self.session.commit()
        QtGui.QMessageBox.information(self,"Modificacion","Modificacion registrada con exito!")
        print "MODIFICADO: ", str(self.elemento_a_modificar)
        self.hide()


"""

DIALOGOS_FORANEAS = """
        self.index_${NOMBRE_CAMPO} = {} #Para recuperar la $NOMBRE_CAMPO del combo seleccionada, sin tener que andar parseando cadenas.
        for index, $NOMBRE_CAMPO in enumerate(${NOMBRE_OBJETO}.buscarTodos(self.session)):
            self.index_${NOMBRE_CAMPO}.update({index: ${NOMBRE_CAMPO}.getId()})
            self.ui.comboBox${NOMBRE_OBJETO}.insertItem(index, str(${NOMBRE_CAMPO}))

"""

#=======================================================#
# Constantes utiles
#=======================================================#
MODELO_TABLA_UTILES = """from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


class ModeloTabla(QAbstractTableModel):
    '''
    Modelo abstracto.
    @params:
        - datain: datos de la tabla. Por ej:
            data = [['00','01','02'],
                    ['10','11','12'],
                    ['20','21','22']]
        - headers: Lista de nombres de las cabeceras. Por ejemplo
            headers = ['Nombre', 'Apellido', 'DNI']
        - contenido: string que define lo que contiene la tabla. Se muestra en la columna vertical izquierda.
    '''
    def __init__(self, datain, headers, contenido='Producto', parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.__data = datain
        self.__headers = headers
        self.__contenido = contenido

    def rowCount(self, parent):
        return len(self.__data)

    def columnCount(self, parent):
        return len(self.__data[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.__data[index.row()][index.column()])

    def headerData(self, section, orientation, role):
        
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"
            else:
                return QString(self.__contenido+" %1").arg(section)


"""

WIDGET_ABM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Widget_ABM</class>
 <widget class="QWidget" name="Widget_ABM">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>495</width>
    <height>375</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>ABM</string>
  </property>
  <layout class="QHBoxLayout" name="horizontalLayout_2">
   <item>
    <spacer name="horizontalSpacer">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="sizeType">
      <enum>QSizePolicy::Minimum</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>40</width>
       <height>20</height>
      </size>
     </property>
    </spacer>
   </item>
   <item>
    <layout class="QVBoxLayout" name="verticalLayout">
     <item>
      <spacer name="verticalSpacer_4">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
       <property name="sizeType">
        <enum>QSizePolicy::Minimum</enum>
       </property>
       <property name="sizeHint" stdset="0">
        <size>
         <width>20</width>
         <height>40</height>
        </size>
       </property>
      </spacer>
     </item>
     <item>
      <widget class="QLabel" name="labelTitulo">
       <property name="text">
        <string>TEXTO LABEL</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QGroupBox" name="groupBox">
       <property name="title">
        <string/>
       </property>
       <layout class="QHBoxLayout" name="horizontalLayout">
        <item>
         <widget class="QTableView" name="tableViewData"/>
        </item>
        <item>
         <layout class="QVBoxLayout" name="verticalLayout_2">
          <item>
           <spacer name="verticalSpacer">
            <property name="orientation">
             <enum>Qt::Vertical</enum>
            </property>
            <property name="sizeHint" stdset="0">
             <size>
              <width>20</width>
              <height>40</height>
             </size>
            </property>
           </spacer>
          </item>
          <item>
           <widget class="QPushButton" name="pushButtonEliminar">
            <property name="text">
             <string>Eliminar</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="pushButtonModificar">
            <property name="text">
             <string>Modificar</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="pushButtonNuevo">
            <property name="text">
             <string>Nuevo...</string>
            </property>
           </widget>
          </item>
          <item>
           <spacer name="verticalSpacer_2">
            <property name="orientation">
             <enum>Qt::Vertical</enum>
            </property>
            <property name="sizeHint" stdset="0">
             <size>
              <width>20</width>
              <height>40</height>
             </size>
            </property>
           </spacer>
          </item>
         </layout>
        </item>
       </layout>
      </widget>
     </item>
     <item>
      <spacer name="verticalSpacer_3">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
       <property name="sizeType">
        <enum>QSizePolicy::Preferred</enum>
       </property>
       <property name="sizeHint" stdset="0">
        <size>
         <width>20</width>
         <height>40</height>
        </size>
       </property>
      </spacer>
     </item>
    </layout>
   </item>
   <item>
    <spacer name="horizontalSpacer_2">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="sizeType">
      <enum>QSizePolicy::Minimum</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>40</width>
       <height>20</height>
      </size>
     </property>
    </spacer>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

CENTRAL_WIDGET_ABM = """import sys
sys.path.append('..')
from forms.c_widgetABM import Ui_Widget_ABM
from PyQt4 import QtCore, QtGui

from base_de_datos.conexion import Conexion
#Manejo de objetos:
from base_de_datos.models import Producto ,Retiro ,Categoria ,Ingreso #Por ejemplo: Categoria, Producto

#Modelo de la table view del dialogo:
from ModeloTabla import ModeloTabla

class FormABM(QtGui.QWidget):
    '''
    Widget generico. Lista objetos y permite ABM
    @params:
        - parent.
        - clase: Clase del modelo sobre la cual se esta realizando ABM.
        - callback_baja: funcion que se va a ejecutar cuando se haga click en el boton Eliminar del widget.
        - callback_modificar: funcion que se va a ejecutar cuando se haga click en el boton Modificar del widget.
        - callback_alta: funcion que se va a ejecutar cuando se haga click en el boton Nuevo... del widget.
    '''
    def __init__(self, parent=None, clase=None, callback_baja=None, callback_modificar=None, callback_alta=None):
        super(FormABM, self).__init__(parent)
        self.parent = parent
        self.ui = Ui_Widget_ABM()
        self.ui.setupUi(self)
        self.session = Conexion.getSession()

        if clase:
            self.ui.labelTitulo.setText(QtCore.QString('%ss' % clase.__name__))

        self.clase = clase
        self.elementos_indexes = {} #lleva el control indice_tabla - id_producto
        self.actualizarDatosTabla()

        self.callback_baja = callback_baja
        self.callback_modificar = callback_modificar
        self.callback_alta = callback_alta
        self.ui.pushButtonEliminar.clicked.connect(self.on_baja)
        self.ui.pushButtonModificar.clicked.connect(self.on_modificar)
        self.ui.pushButtonNuevo.clicked.connect(self.on_alta)

    def on_baja(self):
        #beautiful spanglish
        self.callback_baja(self.elemento_seleccionado())
        self.actualizarDatosTabla()        

    def on_modificar(self):
        #beautiful spanglish
        self.callback_modificar(self.elemento_seleccionado())

    def on_alta(self):
        #beautiful spanglish
        self.callback_alta(self.elemento_seleccionado())
  
    def elemento_seleccionado(self):
        index = self.ui.tableViewData.selectedIndexes()[0].row()
        elemento_seleccionado = self.clase.buscarPorID(self.session, self.elementos_indexes.get(index))
        return elemento_seleccionado

  
    def actualizarDatosTabla(self):
        #*Llenar la tabla de elementos:
        elementos_all = self.clase.buscarTodos(self.session)
        #**enviar al table model una lista de listas con los datos de los elementos:
        elementos = []
        headers = []
        for index, elemento in enumerate(elementos_all):
            self.elementos_indexes.update({index:elemento.getId()}) #En el indice actual, va el elemento con el id...
            # elementos.append([
            #                 elemento.getId(),
            #                 elemento.nombre,
            #                 elemento.descripcion,
            #                 elemento.stock
            #                 ])
            elementos.append(elemento.valores_de_campos())
            # headers = ['ID', 'Nombre', 'Descripcion', 'Stock']
            headers = elemento.nombres_de_campos()

        if not elementos:
            elementos = ['---']
            headers = ['La tabla no posee elementos.']
        print "ENVIANDO ELEMENTOS: ", elementos
        print "ENVIANDO headers: ", headers
        tablemodel = ModeloTabla(elementos, headers, self.clase.__name__, self)
        self.ui.tableViewData.setModel(tablemodel)
        self.ui.tableViewData.selectRow(0) #Para que haya al menos una fila elegida por defecto
        self.ui.tableViewData.setSelectionMode(QtGui.QAbstractItemView.SingleSelection) #para que no se puedan seleccionar multiples filas
        self.ui.tableViewData.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

"""