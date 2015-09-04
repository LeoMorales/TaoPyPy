****************************************
TaoPyPy
****************************************

Automatizador/ahorrador de pasos comunes para crear una app python que use PyQt...
En resumen, recibe un archivo xml, al cual analiza y en base a él crea las tablas, objetos e interfaz básica necesaria.


-------------------
Ejemplo basico:
-------------------

Tenemos nuestro data.xml:

.. code-block:: html

    <?xml version="1.0"?>
    <data>
        <meta>
            <nombreBD>productosBD</nombreBD>
            <tipoBD>SQLite</tipoBD>
        </meta>
        <tabla nombre="producto">
            <campo clave="true">id_producto</campo>
            <campo tipo="CharField" tamanio="50">nombre</campo>
            <campo tipo="CharField" tamanio="150">descripcion</campo>
            <campo tipo="IntegerField">stock</campo>
            <campo tipo="ForeignKey">categoria</campo>
            
        </tabla>
        <tabla nombre="categoria">
            <campo clave="true">id_categoria</campo>
            <campo tipo="CharField" tamanio="50">nombre</campo>
            <campo tipo="CharField" tamanio="150">descripcion</campo>
        </tabla>
        <tabla nombre="retiro">
            <campo clave="true">id_retiro</campo>
            <campo tipo="CharField" tamanio="100" label="Retira">quien_retira</campo>
            <campo tipo="CharField" tamanio="150">motivo</campo>
            <campo tipo="IntegerField">cantidad</campo>
            <campo tipo="DateField">fecha</campo>
            <campo tipo="ForeignKey">producto</campo>
        </tabla>
        <tabla nombre="ingreso">
            <campo clave="true">id_ingreso</campo>
            <campo tipo="CharField" tamanio="100">proveedor</campo>
            <campo tipo="DateField">fecha</campo>
            <campo tipo="IntegerField">cantidad</campo>
            <campo tipo="ForeignKey">producto</campo>
        </tabla>
    </data>


.. code-block:: bash

    $ python taopypy.py --new MiProyecto --dataModelSource path/al/archivo/data.xml

    #Si lo clonaron, directamente:

    $ python taopypy.py --new MiProyecto

El resultado será un proyecto nuevo en la carpeta Proyectos/MiProyecto

Para ver el resultado:

.. code-block:: bash

    $ python2.7 Proyectos/MiProyecto/src/main.py

Tenemos el cascaron de una aplicación.


-------------------
Alcance
-------------------

Version de Python: 2.7

Requerimientos:
    - sqlalchemy
    - PyQt4

Tipos de datos:

    - Entero -> IntegerField
    - Cadena -> CharField
    - Fecha -> DateField
    - Foranea -> ForeignKey (solo uno a muchos...)


-------------------
Trabajo por hacer
-------------------

- Me falta todavía:
    - Agregar funcionalidad de Alta, Modificacion y Borrado a Admin.
    - Una documentación validLA Documentacion.
    - Entre otras cosas...


Basado en un trabajo realizado por Seba Shanz -> http://infortips.blogspot.com.ar/2012/11/framework-python.html

