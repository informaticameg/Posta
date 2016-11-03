#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join,abspath,dirname 
import cStringIO
from PyQt4 import QtCore, QtGui, uic
from plasta.gui.mytablewidget import MyTableWidget
import uis.images_rc
from tools import pathtools

class BaseGUI(QtGui.QMainWindow):
    
    def __init__(self, parent, manager, managers = []):
        QtGui.QMainWindow.__init__(self)
        self.parent = parent
        self.FILENAME = 'plasta/gui/uis/admin.ui'
        ICONFILE = 'images/Searchicon.png'
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(join(abspath(dirname(__file__)),ICONFILE))))#
        self.manager = manager
        self.managers = managers
        self.MyTabla = None
        self.ATRIBUTOSLISTA = None#el orden y la cantidad de atributos en str que quieras
        self.ALINEACIONLISTA = []#la alinecion de cada atributo en la fila
        self.ATRI_COMBO_BUSQUEDA = []#el orden y la cantidad de atributos en str que quieras
        self.DialogAddClass  = None#la clase que invoca a los dialogos de agregar y editar
        self.TITULO = ''
        self.develop = True
        
    def _operaciones_de_inicio(self):
        u'''
        operaciones necesarias para levantar las ventanas
        '''
        self.loadUi()
        #uic.loadUi(self.FILENAME, self)
        self.setWindowTitle(self.TITULO)
        self.lbTitulo.setText(self.manager.getClassName())
        self._makeTable()
        
        self.cargarCombobox()
        self.cargarTabla()
        self._loadAppShortcuts()
        self.fullScreen = False
        
        self._centerOnScreen()

    def _toogleFullScreen(self):
        ''' '''
        if not self.fullScreen :
            self.showFullScreen()
        else:
            self.showNormal()
        self.fullScreen = not self.fullScreen

    def _loadAppShortcuts(self):
        u""" Load shortcuts used in the application. """
        self._atajo_salir = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)
        self._atajo_fullscreen = QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self._toogleFullScreen)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
        
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_N), self, self.on_btAgregar_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_M), self, self.on_btEditar_clicked)
        QtGui.QShortcut(QtGui.QKeySequence("Del"), self, self.on_btEliminar_clicked)
        
    def loadUi(self):
        if self.develop:
            uic.loadUi(self.FILENAME, self)
        else:
            UI_CONTENT = cStringIO.StringIO(self.parent.uis[self.FILENAME])
            uic.loadUi(UI_CONTENT, self)
        
    def on_context_menu(self,point):
        #print point
        mypoint = QtCore.QPoint(point.x()+10,point.y()+30)
        #print mypoint
        self.popMenu = QtGui.QMenu( self )
        #NEXT:ver detalles
        #self.popMenu.addAction("Ver detalles",XXXXXXXXXX ,QtGui.QKeySequence("Ctrl+R"))
        #self.popMenu.addSeparator()
        self.popMenu.addAction("Nuevo",self.on_btAgregar_clicked ,QtGui.QKeySequence("Ctrl+N"))
        self.popMenu.addAction("Modificar",self.on_btEditar_clicked ,QtGui.QKeySequence("Ctrl+M"))
        self.popMenu.addAction("Eliminar",self.on_btEliminar_clicked ,QtGui.QKeySequence("Del"))
        
        self.popMenu.exec_(self.MyTabla.widget.mapToGlobal(mypoint) )
 
    def cargarCombobox(self):
        '''
        carga el combobox de campos
        '''
        self.cbCampos.clear()
        if not self.ATRI_COMBO_BUSQUEDA :
            atributos = self.manager.getClassAttributes()
            for atributo in atributos:
                self.ATRI_COMBO_BUSQUEDA.append({atributo:self._obtaincolumnforname(atributo)})
        map(self.cbCampos.addItem, [p.keys()[0] for p in self.ATRI_COMBO_BUSQUEDA])
            
    def cargarTabla(self,listadeobj = None):
        '''
        carga la lista de objetos en la tabla
        @param listadeobj:if none carga todos, sino lo de la lista
        '''        
        if listadeobj == None:
            listadeobj = self.manager.getall()
        listadefilas = [self._obtenerValoresAtributos(obj) for obj in listadeobj]
        self.MyTabla.addItems(listadefilas)
        try:
            self.setCantidadItems(len(listadeobj))
        except AttributeError :
            pass
        
    def search(self, camponame, valor):
        '''
        @param camponame:el nombre del campo en strin
        @param valor:el valor de el campo(soporta los tipos de datos de searchBy)
        @return: lista de obj
        '''
        return self.manager.searchBy(camponame,valor)

    def actual_rows_to_objects(self):
        '''
        obtiene el objeto que representa la tabla
        @return: un objeto del tipo que maneja self.manager
        '''
        listadelistastring = self.MyTabla.getListSelectedRows()
        atributos_names = self._obtener_atributos_names()
        classid = self.manager.CLASSid
        listadeobjetos = []
        if listadelistastring != []:
            # obtiene el tipo de dato de la clave del objeto
            for value in self.manager.getClassAttributesInfo().values() :
                if value['primary'] == True :
                    primary_type = value['type'] 
            
            for lista in listadelistastring:
                posicion_ide = atributos_names.index(classid)
                if primary_type is 'int' :
                    valor_ide = int(lista[posicion_ide])
                else:
                    valor_ide = lista[posicion_ide]   
                                      
                listadeobjetos.append(self.manager.searchBy(self._obtaincolumnforname(self.manager.CLASSid),valor_ide)[0])
            return listadeobjetos
        return None
    
    def _obtener_atributos_names(self):
        '''
        Obtiene los atributos de la clase que maneja self.manager
        '''
        return self.ATRIBUTOSLISTA_CLASSNAMES if self.ATRIBUTOSLISTA else self.manager.getClassAttributes()
        
    def _makeTable(self):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._obtener_atributos_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.obtenerNombreAtributo( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA]
        self.MyTabla = MyTableWidget(self.twDatos, columnasTablas, self.ALINEACIONLISTA)
        self.connect(self.MyTabla.widget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
 
    def _obtenerValoresAtributos(self,obj):
        resultado = []
        atributos_objeto = self.manager.getClassAttributesValues(obj)
        if not self.ATRIBUTOSLISTA :            
            return atributos_objeto
        else:
            atributos_clase = self.manager.getClassAttributes()
            atributos_ordenados = self.ATRIBUTOSLISTA_CLASSNAMES
            for atributo in atributos_ordenados:
                resultado.append( atributos_objeto[ atributos_clase.index( atributo ) ] )
            return resultado
                
    def getIndexClassId(self):
        """
        Obtiene la posicion en la que se encuentra ubicado el id en la lista de atributos.
        """
        return 
    
    def _obtaincolumnforname(self,columnname):
        '''
        a partir de un string obtiene la columna de storm
        @param columnname:nombre del atributo en str
        @return: 
        '''
        #MAGIC###################
        busqueda = self.manager.CLASS.__dict__[columnname]
        if str(type(busqueda)) != "<class 'storm.references.Reference'>" :             
            try:
                campo = self.manager.CLASS.__dict__['_storm_columns'][busqueda]
            except:
                # print "no tengo idea del error gui-_obtaincolumnforname"
                campo = busqueda
        else:
            campo = busqueda
        #END MAGIC###############
        return campo
        
    def _buscar(self):
        '''
        junta los datos, reliza la busqueda y carga la tabla
        '''
        valor = unicode(self.leBusqueda.text().toUtf8(),'utf-8')
        if valor != u'' :            
            self.recargarLista()
        else:
            self.cargarTabla()
    
    def recargarLista(self):
        valor = unicode(self.leBusqueda.text().toUtf8(),'utf-8')
        campo = unicode(self.cbCampos.itemText(                                               
                    self.cbCampos.currentIndex()).toUtf8())    
        if self.ATRI_COMBO_BUSQUEDA :
            campo = [p[campo] for p in self.ATRI_COMBO_BUSQUEDA if campo in p ][0]
        else:
            campo = self._obtaincolumnforname(campo)
        resultado = self.search(campo,valor)
        self.cargarTabla(resultado)
        self._setSearchColor(self.leBusqueda, resultado)
        
    def _setSearchColor(self, widget, resultados_busqueda):
        color_rojo = 'background-color: rgb(255, 178, 178);' 
        try:
            if self.myStyleSheetBlanco == '' : 
                if not widget.styleSheet().isEmpty() :
                    style = widget.styleSheet()
                    self.myStyleSheetBlanco = widget.styleSheet()        
                                
                    pos1 = style.indexOf('QLineEdit')
                    pos2 = style.indexOf('}',pos1)
                    style = style.replace(pos2,1,color_rojo + '}')
                    self.myStyleSheetRojo = style
                else:
                    self.myStyleSheetRojo = color_rojo
                        
            if not widget.text().isEmpty() :
                if len(resultados_busqueda) == 0 :
                    widget.setStyleSheet(self.myStyleSheetRojo)
                else:
                    widget.setStyleSheet(self.myStyleSheetBlanco)
            else:
                widget.setStyleSheet(self.myStyleSheetBlanco)
        except:
            self.myStyleSheetBlanco = ''
            self.myStyleSheetRojo = ''
            self._setSearchColor(widget, resultados_busqueda)
                
##############################
# METODOS PARA REIMPLEMENTAR #
##############################

    def agregar(self):
        #REIMPLEMENT
        return self.DialogAddClass(self.parent, self.manager, itemaeditar = False, managers = self.managers)
    
    def editar(self, obj):
        #REIMPLEMENT
        return self.DialogAddClass(self.parent, self.manager, itemaeditar = obj, managers = self.managers)

    def eliminar(self, obj):
        #REIMPLEMENT
        self.manager.delete(obj)

##########################
# METODOS DE LOS EVENTOS #
########################## 

    def setCantidadItems(self, valor):
        self.lbCantidadItems.setText( str(valor) + ' items(s) listados(s)')
        
    def on_leBusqueda_textChanged(self, texto):
        self._buscar()
        
    @QtCore.pyqtSlot(int)
    def on_cbCampos_currentIndexChanged (self,entero):
        if not self.leBusqueda.text().isEmpty() :
            self._buscar()
    
    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self):
        wAgregar = self.agregar()
        wAgregar.postSaveMethod = self.recargarLista
        wAgregar.exec_()
    
    @QtCore.pyqtSlot()
    def on_btEditar_clicked(self):
        listadeobjetosseleccionados = self.actual_rows_to_objects()
        if listadeobjetosseleccionados:
            for obj in listadeobjetosseleccionados:
                wEditar = self.editar(obj)
                wEditar.postSaveMethod = self.recargarLista 
                wEditar.exec_()

    @QtCore.pyqtSlot()
    def on_btEliminar_clicked(self):
        listadeobjetosseleccionados = self.actual_rows_to_objects()
        if listadeobjetosseleccionados:
            for obj in listadeobjetosseleccionados:
                result = QtGui.QMessageBox.warning(self, u"Eliminar "+ self.manager.getClassName(),
                    u"¿Esta seguro que desea eliminar?.\n\n",
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if result == QtGui.QMessageBox.Yes:
                    self.eliminar(obj)
                    self._buscar()

    def on_twDatos_doubleClicked(self , index):
        pass
    
#########
# OTROS #
#########

    def _centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
