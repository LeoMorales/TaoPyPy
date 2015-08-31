FORANEA = 'ForeignKey'
ENTERO = 'IntegerField'
CADENA = 'CharField'
FECHA = 'DateField'

class Tabla(object):
	"""docstring for Tabla"""
	def __init__(self, nombre, campos=[]):
		super(Tabla, self).__init__()
		self.nombre = nombre
		self.campos = campos
		# print self
		print "CREADA: ", self.info()

	def nuevoCampo(self, nuevo):
		self.campos.append(nuevo)

	def __str__(self):
		return "-> Tabla: {}".format(self.nombre)

	def info(self):
		return "{}\nCampos: {}".format(str(self), "\n".join(['%s%s'%(type(c), c.nombre) for c in self.campos]))

	def camposSinClave(self):
		return [campo for campo in self.campos if not campo.esClave()]

	def tieneForaneas(self):
		return len(self.clavesForaneas()) > 0

	def clavesForaneas(self):
		return filter(lambda campo: campo.esForanea(), self.campos)

	def campos_para_creacion(self):
		return ", ".join([campo.get_nombre() for campo in self.campos if not campo.esClave()])


class Campo(object):
	"""docstring for Campo"""
	def __init__(self, nombre, tipo, es_clave=False, tamano=None, label=''):
		super(Campo, self).__init__()
		self.nombre = nombre
		#Lo siguiente seria metadata del campo:
		self.tipo = tipo
		# self.valor = valor
		self.es_clave = es_clave
		self.tamano = 50 if (not tamano and tipo == CADENA) else tamano
		# print self
		self.label = label

	def esForanea(self):
		if not self.tipo:
			return False
		return self.tipo == FORANEA
	
	def esClave(self):
		return self.es_clave

	def data(self):
		return {'nombre': self.nombre,
				'tipo': self.tipo,
				'clave': self.es_clave,
				'tamano': self.tamano
				}

	def __str__(self):
		return "-> Campo: {nombre} Tipo: {tipo} Clave: {clave} Tamano: {tamano}: ".format(**self.data())

	def representacion_en_columna(self):
		'''
		Retorna la representacion de campo como columna de una Tabla de sqlalchemy
		'''
		if self.esClave():
			return "                Column('id', Integer, primary_key=True)"
		elif self.tipo == CADENA:
			return "                Column('{}', String({}))".format(self.nombre, self.tamano)
		elif self.tipo == FECHA:
			return "                Column('{}', DateTime, default=func.now())".format(self.nombre)
		elif self.tipo == ENTERO:
			return "                Column('{}', Integer)".format(self.nombre)
		elif self.tipo == FORANEA:
			return "                Column('{}', Integer, ForeignKey('{}.id'))".format(self.nombre+'_id', self.nombre)#en data.xml debe ser <campo tipo="foranea">persona</campo>, por ejemplo.

		#sino:
		return "{} tipo de campo invalido".format(self.nombre)

	def get_nombre(self):
		if self.tipo == FORANEA:
			return self.nombre+'_id'
		return self.nombre

	def representacion_widget(self):
		representacion = {
			FORANEA: "<widget class='QComboBox' name='comboBox{}'/>".format(self.nombre.capitalize()),
			ENTERO:"<widget class='QSpinBox' name='spinBox{}'/>".format(self.nombre.capitalize()),
			CADENA: "<widget class='QLineEdit' name='lineEdit{}'/>".format(self.nombre.capitalize()),
			FECHA: "<widget class='QCalendarWidget' name='calendarWidget{}'/>".format(self.nombre.capitalize())
		}
		return representacion[self.tipo]

	def representacion_obtencion_dialogo(self):
		representacion = {
			FORANEA: "{}_id = self.index_{}.get(self.ui.comboBox{}.currentIndex())".format(self.nombre, self.nombre, self.nombre.capitalize()),
			ENTERO:"{} = self.ui.spinBox{}.value()".format(self.nombre, self.nombre.capitalize()),
			CADENA: "{} = str(self.ui.lineEdit{}.text())".format(self.nombre, self.nombre.capitalize()),
			FECHA: "{fecha} = self.ui.calendarWidget{fecha_capitalizada}.selectedDate()\n        from datetime import datetime\n        {fecha} = datetime({fecha}.year(), {fecha}.month(), {fecha}.day(), 9, 0, 0)".format(**{'fecha': self.nombre, 'fecha_capitalizada': self.nombre.capitalize()})
		}
		return representacion[self.tipo]		

class Manager(object):
	"""docstring for Manager"""
	def __init__(self, nombreBD, tipoBD, tablas=[]):
		super(Manager, self).__init__()
		self.nombreBD = nombreBD
		self.tipoBD = tipoBD
		self.tablas = tablas
		
	def nuevaTabla(self, tabla):
		self.tablas.append(tabla)

	def strStatus(self):
		return "Manager contiene {} tablas\nTABLAS: {}".format(len(self.tablas), '\n'.join([t.info() for t in self.tablas]))

	def nombres_tablas_para_models(self):
		return " ,".join([t.nombre.capitalize() for t in self.tablas])

	def nombres_tablas_para_dmodels(self):
		return " ,".join(["d%s"%t.nombre.capitalize() for t in self.tablas])