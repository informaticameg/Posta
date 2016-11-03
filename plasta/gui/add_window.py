#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic
import PyQt4
import cStringIO

class BaseAddWindow(QtGui.QDialog):
    
    def __init__(self, parent, unManager, itemaeditar = False, managers = []):
        QtGui.QDialog.__init__(self)
        self.parent = parent   
        self.manager = unManager
        self.managers = managers
        self.EDITITEM = itemaeditar
                
        self.ITEMLIST = []        
        self.dict_referencias = {} # diccionario que contiene la instancia seleccionada en el buscador
        self.postSaveMethod = None # metodo que BaseGUI que se ejecuta luego de guardar() 
        self._dictWidgetReferencias = {} # diccionario que contiene los widget boton y la referencia a la cual pertenece
    
##########################
# METODOS DE LOS EVENTOS #
##########################    
    
    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        resultado = False
        if self.validarRestriccionesCampos() :
            datos = self.obtenerDatosWidgets()
            resultado = self.guardar(datos) if not self.EDITITEM else self.editar(datos)
            if self.postSaveMethod :
                self.postSaveMethod()        
            self._mostrarMensajeResultado(resultado)
            self.close()
        return resultado
    
    def _mostrarMensajeResultado(self, resultado):
        if not self.EDITITEM:
            if resultado :            
                QtGui.QMessageBox.information(self, "Agregar "+self.getNombreClase(),self.getNombreClase()+u" agregado con éxito.")
            else:
                QtGui.QMessageBox.warning(self, "Agregar "+self.getNombreClase(),"No se pudo agregar el "+self.getNombreClase())
        else:
            if resultado :
                QtGui.QMessageBox.information(self, "Editar " +self.getNombreClase(),self.getNombreClase()+" editado con exito.")
            else:
                QtGui.QMessageBox.warning(self, "Editar "+self.getNombreClase(),"No se pudo editar el "+self.getNombreClase())        
        
    @QtCore.pyqtSlot()
    def on_btSalir_clicked(self):
        self.close()
        
######################
# METODOS AUXILIARES #
######################  

    def loadUi(self):
        UI_CONTENT = cStringIO.StringIO(self.parent.uis[self.FILENAME])
        uic.loadUi(UI_CONTENT, self)

    def agregarValidadores(self):
        infoclase = self.manager.getClassAttributesInfo()
        for dato in self.ITEMLIST:
            widget = dato.keys()[0]
            atributo_clase = dato.values()[0]
            nombrecolumnalabel = "lb"+[k for k, v in self.__dict__.iteritems() if v == widget][0][2:]  
            if str(type(atributo_clase)) == "<class 'storm.references.Reference'>" : 
                try:
                    if widget is QtGui.QLineEdit :
                        widget.setReadOnly(True)
                    # conecta el evento al boton de una referencia
                    nombreboton = "bt" + [k for k, v in self.__dict__.iteritems() if v == widget][0][2:]
                    widgetboton = self.__dict__[nombreboton]
                    self._dictWidgetReferencias[ widgetboton ] = atributo_clase
                    self.connect(widgetboton, QtCore.SIGNAL('clicked ()'),self.mostrarBuscador)
                except KeyError, msg:
                    print 'KeyError: Posiblemente no has agregado el boton para elegir una referencia.\nMensaje del error: ' + str(msg)
            else:
                columnastorm = self.manager.propertyToColumn(atributo_clase)
                if infoclase[columnastorm]["type"] == 'str':
                    pass
                elif infoclase[columnastorm]["type"] == 'int':
                    if type(widget) is QtGui.QLineEdit :
                        widget.setValidator(QtGui.QIntValidator())
                    
                if infoclase[columnastorm]["null"] == False:
                    try:
                        label = self.__dict__[nombrecolumnalabel]
                        label.setText(label.text()+u'*')
                        # setea el color de fondo indicando que es una campo obligatorio
                        widget.setStyleSheet('background-color: rgb(223, 221, 255);')
                    except KeyError, msg:
                        # print 'ERROR al intentar validar las restricciones para <%s>' % nombrecolumnalabel
                        # print 'KeyError: Posiblemente el widget QLabel se llama de otra manera.'
                        # print 'SOLUCION: Debe llamarce de la misma manera que el atributo de la clase.'
                        pass
                if infoclase[columnastorm]["default"] != None:
                    #NEXT:poner valor por defecto
                    pass
                
                if infoclase[columnastorm]["primary"] == True:
                    label = self.__dict__[nombrecolumnalabel]
                    label.setText(label.text()+u'*')
                    #NEXT:not null
                    # setea el color de fondo indicando que es una campo obligatorio
                    widget.setStyleSheet('background-color: rgb(223, 221, 255);')

    def validarRestriccionesCampos(self):
        """
        Comprueba que los campos que son <primary key> y <allow none = False>, 
        no esten vacios a la hora de guardar. 
        """
        
        valido = True 
        color_rojo = 'background-color: rgb(255, 178, 178);'
        
        # 1° obtener la informacion de los atributos
        # 2° obtener a partir de los atributos, los properties 
        # 3° a partir de los properties obtener los widgets
        def filtrarAtributos(informacion):
            info_que_necesito = filter( 
                    lambda atributo : True if ((atributo['primary'] == True) or (atributo['null'] == False)) else False,
                    informacion.values())
            return map(lambda atri : self.obtenerKeyDiccionario(informacion, atri), info_que_necesito)
            
        # obtiene los atributos que poseen restricciones
        atributes = filtrarAtributos( self.manager.getClassAttributesInfo() ) 
        # obtiene los widgets y ya setea el color en cas
        for atributo in atributes :
            for item in self.ITEMLIST :                
                if not str(type(item.values()[0])) == "<class 'storm.references.Reference'>" :
                    if self.manager.propertyToColumn(item.values()[0]) == atributo :
                        widget = item.keys()[0]
            
                        if type(widget) is QtGui.QLineEdit :
                            if widget.text().isEmpty() :
                                valido = False
                        elif type(widget) is QtGui.QTextEdit :
                            if widget.toPlainText().isEmpty() :
                                valido = False
                        elif type(widget) is QtGui.QDoubleSpinBox :
                            if widget.value() <= 0.0 :
                                valido = False
                        if not valido :
                            widget.setStyleSheet( color_rojo )
        return valido
        
    def obtenerKeyDiccionario(self, dic, val):
        """return the key of dictionary dic given the value"""
        return [k for k, v in dic.iteritems() if v == val][0]
    
    def obtenerDatosWidgets(self):
        '''
        Obtiene los datos de las widget contenidos
         en las claves de ITEMLIST
        @return: lista de valores
        '''
        from PyQt4.QtGui import QIntValidator,QLineEdit,QComboBox,QLabel,QDateEdit,QTextEdit,QSpinBox,QCheckBox,QDoubleSpinBox
        
        def unicodesimple(dato):
            return unicode(dato.toUtf8(),'utf-8')
        
        def esCheckBox(widget):
            return widget.isChecked()
            
        def esSpinBox(widget):
            return widget.value()
            
        def esTextEdit(widget):
            return unicodesimple( widget.toPlainText() )
        
        def esLineedit(widget):
            if type(widget.validator()) == QIntValidator:
                if not widget.text().isEmpty() :                    
                    value = int(esLabel(widget))
                else:
                    value = None
            else:
                value = esLabel(widget)
            return value

        def esDateEdit(widget):
            return unicodesimple(widget.date().toString(widget.displayFormat()))

        def esCombobox(widget):
            return unicodesimple(widget.itemText(widget.currentIndex()))
                
        def esLabel(widget):
            return unicodesimple(widget.text())
        
        def esQDoubleSpinBox(widget):            
            return widget.value()
        
        def esQPlainTextEdit(widget):            
            return widget.value()
            
        funcionwidget = {QLineEdit:esLineedit,QComboBox:esCombobox,QLabel:esLabel,
                        QDateEdit:esDateEdit,QTextEdit:esTextEdit,QSpinBox:esSpinBox,
                        QCheckBox:esCheckBox,QDoubleSpinBox:esQDoubleSpinBox}

        values = []
        for dicci in self.ITEMLIST:
            widget = dicci.keys()[0]
            if not(widget in self.dict_referencias):
                valor = funcionwidget[type(widget)](widget)
            else:
                valor = self.dict_referencias[widget]            
            values.append(valor) if valor != u'' else values.append(None) #@NoEffect
        return values
    
    def obtenerDatosIntancia(self):
        '''
        Obtiene los datos de los atributos contenidos
        en los valores de ITEMLIST del obj EDITITEM
        @requires: usar storm
        @return: lista de datos [{nombreatributo,valor}] o false(si no hay EDITITEM)
        '''
        if not self.EDITITEM:
            return False
        listcolumns = []
        import storm
        for v in self.ITEMLIST:
            if type(v.values()[0]) == storm.references.Reference:
                self.dict_referencias[v.keys()[0]] = self.EDITITEM.__getattribute__(
                    self.manager._obtenerNombreReference(v.values()[0]))
            listcolumns.append(v.values()[0])
        return self.manager.getDataObject(self.EDITITEM,listcolumns)
        
    def getNombreClase(self):
        '''
        @requires: usar storm
        @return: el nombre de la clase que maneja el manager
        '''
        return self.manager.getClassName()

    def editarPropiedades(self):
        '''
        obtiene los datos de EDITITEM y los de los widgets
        los compara y si son distintos edita el atributo del obj
        '''
        datos = self.obtenerDatosWidgets()
        propiedadesvalues = self.obtenerDatosIntancia()
        for i,dato in enumerate(datos):
            nombrepropiedad = propiedadesvalues[i].keys()[0]
            valor = propiedadesvalues[i].values()[0]
            if valor != dato:
                self.EDITITEM.__setattr__(nombrepropiedad,dato) 
        return True       

    def guardar(self, listadedatos):
        '''
        Metodo que automatiza el guardado de los datos.
        @param listadedatos:lista de datos perteneciente al init de la clase que maneja
        '''
        #REIMPLEMENT
        return self.manager.add(*listadedatos)
    
    def editar(self, listadedatos):
        '''
        Metodo que automatiza el editar de los datos.
        @param listadedatos:lista de datos perteneciente al init de la clase que maneja
        '''
        #REIMPLEMENT
        try:
            self.editarPropiedades()
            self.manager.almacen.commit()
            return True
        except Exception,e:
            print 'editar ERROR: ', e
            return False
 
    def _operaciones_de_inicio(self):
        '''
        operaciones que se requieren para iniciar la ventana
        '''
        self._centerOnScreen()
        self.agregarValidadores()
        self.btGuardar.setDefault(True)
        if self.EDITITEM:
            self.btGuardar.setText('Editar')
            self.setWindowTitle(u'Editar '+self.manager.getClassName())
            self._cargarDatosinWidgets()
        else:
            self.setWindowTitle(u"Agregar " + self.manager.getClassName())
    
    def _cargarDatosinWidgets(self):
        '''
        carga los datos de el obj EDITITEM en sus correspondientes
        widgets marcados por ITEMLIST
        '''
        import PyQt4
        import datetime
        for propnombre,propvalue in enumerate(self.obtenerDatosIntancia()):
            widget = self.ITEMLIST[propnombre].keys()[0]
            dato = propvalue.values()[0]
            if not dato is  None :
                tipo = type(widget)            
                if tipo is PyQt4.QtGui.QLineEdit :
                    widget.setText(unicode(str(dato),'utf-8'))
                elif tipo is PyQt4.QtGui.QComboBox:
                    try:
                        widget.setCurrentIndex(widget.findText(dato))
                    except TypeError:
                        widget.setCurrentIndex(widget.findText(dato.__str__()))
                elif tipo is PyQt4.QtGui.QLabel:
                    widget.setText(dato)
                elif tipo is PyQt4.QtGui.QTextEdit:
                    widget.setText(dato)
                elif tipo is PyQt4.QtGui.QSpinBox:
                    widget.setValue(int(dato))
                elif tipo is PyQt4.QtGui.QDoubleSpinBox:
                    widget.setValue(float(dato))
                elif tipo is PyQt4.QtGui.QDateEdit:                    
                    if (type(dato) is unicode) or (type(dato) is str):
                        try:
                            widget.setDate(QtCore.QDate(datetime.date.today().year, int(dato[3:]), int(dato[:-3])))
                        except ValueError:
                            widget.setEnabled(False)
                elif type(dato) is datetime.date :
                        widget.setDate(QtCore.QDate(dato.year, dato.month, dato.day))
        return True
            
    def _centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
                  
    def _toUnicode(self, MyQString):
        '''
        convierte un string a unicode
        @param MyQString:QString a convertir
        @return: unicode value
        '''
        return unicode(MyQString.toUtf8(),'utf-8')
        
    def mostrarBuscador(self):
        """
        A partir de un atributo de la clase
        """
        atributo = self._dictWidgetReferencias[self.sender()]
        # obtener el atributo remoto al que pertenece <atributo>
        all_info = self.manager.getClassAttributesInfo()
        for info_atributo in all_info :            
            if all_info[info_atributo]['reference'] != False :  #@attention: DON'T TOUCH 
                if all_info[info_atributo]['reference']['reference_instance'] is atributo :
                    atributo_remoto = all_info[info_atributo]['reference']['remote_key']
        # obtener el manager al que pertenece <atributo_remoto>
        manager_que_busco = None
        for unmanager in self.managers:        
            if atributo_remoto.__dict__['cls'] == unmanager.CLASS:
                manager_que_busco = unmanager
        # llamar a la ventana del buscador, pasandole el manager        
        from buscador import BaseBuscador
        self.dict_referencias[ self.referenceToWidget(atributo) ] = None
        search = BaseBuscador(manager_que_busco, self.dict_referencias)
        search.exec_()        
         
    def referenceToWidget(self, referencia):
        """
        A partir de una referencia, obtiene el widget correspondiente que es usado por esa referencia.
        """
        for dicti in self.ITEMLIST:
            if dicti.values()[0] is referencia :
                return dicti.keys()[0]
