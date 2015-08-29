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

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(STYLES)

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

DIALOGOS_MAIN = """from forms.c_widgetAlta${NOMBRE_OBJETO} import Ui_FormAlta${NOMBRE_OBJETO}
from PyQt4 import QtCore, QtGui

class FormAlta${NOMBRE_OBJETO}(QtGui.QWidget):
    '''Agregar la funcionalidad del widget'''
    def __init__(self, parent):
        super(FormAlta${NOMBRE_OBJETO}, self).__init__(parent)
        self.parent = parent
        self.ui = Ui_FormAlta${NOMBRE_OBJETO}()
        self.ui.setupUi(self)

"""