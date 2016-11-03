#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import * #@UnusedWildImport
from sqlite3 import OperationalError
import storm


class BaseManager(object):
    '''
    Clase base para manager de una clase storm
    @param seachname: atributo por el cual buscara el metodo get()
    @param reset: si es true limpia y crea la bd  
    '''
    def __init__(self,almacen,reset = False):
        ''''''
        #@param CLASS: la clase que va a manipular ej:Cliente
        self.CLASS = None 
        #@param searchname: lacolumna por la cual el metodo get hace la busqueda ej=Cliente.nombres
        self.searchname = None 
        #@param ATRIBUTOSCLASE: las columnas que va usar (DONTTOUCH)
        self.ATRIBUTOSCLASE = []        
        #@param almacen: el objeto STORE de storm 
        self.almacen = almacen
        #@param reset: variable que determina si se va a resetear 
        self.reset = reset
        
    def _operaciones_de_inicio(self):
        '''
        operaciones que se requieren para iniciar el manager
        '''
        if self.reset:
            self._reset()        
        print "Manager de %s levantado correctamente" % self.CLASS

        #@param CLASSid: la clave primaria de la clase ej:"ide"        
        self.CLASSid = self.getClassIdString()
        
#=======================================================================
# Methods exclusive Plasta 
#=======================================================================
        
    def _obtenerNombreProperty(self,propiedad):
        '''
        devuelve el nombre de on objeto property
        @param propiedad:el objeto property de storm
        '''
        stormcolumns = propiedad.cls.__dict__["_storm_columns"]
        for key in stormcolumns:
            if stormcolumns[key] is propiedad:
                for nombre in propiedad.cls.__dict__:
                    if propiedad.cls.__dict__[nombre] is key:
                        return nombre
        return False
        
    def _reset(self):
        '''
        borra y vuelve a crear la tabla 
        '''
        possiblesvaluestype = {
            "str":"VARCHAR",
            "int":"INTEGER",
            "reference":"INTEGER",
            "date":"VARCHAR",
            "float":"FLOAT",
            "bool":"INT",
            'datetime':'VARCHAR'
        }
        possiblesvaluesprimary = {False:"",True:"PRIMARY KEY"}
        possiblevaluesnull = {False:"NOT NULL",True:""}
        #NEXT: investigar y agregar default...
        
        info =  self.getClassAttributesInfo()
        #CREO EL SQL DINAMICAMENTE
        tablestring = "("
        for columna in info:
            name = info[columna]["name"] if info[columna]["reference"] is False else info[columna]["name"]+"_id"
            
            elemento = (name + " " +
                possiblesvaluestype[info[columna]["type"]] +" " +
                possiblesvaluesprimary[info[columna]["primary"]] +
                possiblevaluesnull[info[columna]["null"]]+",\n")
            tablestring += elemento
        tablestring = tablestring[:-2]+ ")"
        nombredetabla = self.CLASS.__storm_table__
        #ELIMINO LA TABLA
        try:
            self.almacen.execute('DROP TABLE '+nombredetabla)
        except Exception, e:
            print e
        #CREO NUEVAMENTE LA TABLA
        self.almacen.execute('CREATE TABLE '+nombredetabla+' '+tablestring)
        self.almacen.commit()

    def getClassName(self):
        '''
        devuelve el nombre de la clase que maneja
        @return: str
        '''
        return self.CLASS.__name__
    
    def getClassAttributes(self):
        '''
        Obtiene los atributos de la clase que maneja self.manager
        @return: una lista con los atributos de la clase
        '''
        if not self.ATRIBUTOSCLASE:
            itemAexcluir = ('__storm_table__','__module__',
               '__storm_class_info__','__weakref__',
               '_storm_columns','__dict__',
               '__doc__','__init__','SQLTABLE','__str__')
            allAtributes = self.CLASS.__dict__
            for key in allAtributes:
                if not(key in itemAexcluir) and key [-3:] != "_id":
                    self.ATRIBUTOSCLASE.append(key)
        return self.ATRIBUTOSCLASE

    def getClassAttributesInfo(self):
        '''
        Devuelve un diccionario con los tipos de datos de la clase
        @requires: storm
        @return:un diccionario clave:la columna, valor otro diccionario:
        ex:{<storm.properties.Unicode object at 0x9e87b0c>: {'name':'un_atributo','default': None, 'null': True, 'type': 'str', 'primary': False,'reference':False}}
        '''
        resultado={}
        todelete = []
        for name in self.getClassAttributes(): #obtengo los nombe de atributos validos
            objcolumn = self.CLASS.__dict__[name]
            unainfo = {}
            if type(objcolumn) == storm.references.Reference:
                unainfo["type"]= 'reference'
                todelete.append(objcolumn)#eliminar _id
                try:#Fix para cuando sale una tupla en vez de un column (no tengo idea por que es)
                    unainfo["reference"] = {"remote_key":objcolumn.__dict__["_remote_key"][0],"reference_instance":objcolumn}
                    objcolumn = self.propertyToColumn(objcolumn.__dict__["_local_key"][0])#dar los demas datos de ID
                except:
                    unainfo["reference"] = {"remote_key":objcolumn.__dict__["_remote_key"],"reference_instance":objcolumn}
                    objcolumn = objcolumn.__dict__["_local_key"]#dar los demas datos de ID
                
            else:
                unainfo["reference"] = False
                types = {
                    storm.properties.Unicode : 'str',
                    storm.properties.Int : 'int',
                    storm.properties.Bool : 'bool',
                    storm.properties.Date : 'date',
                    storm.properties.Float : 'float',
                    storm.properties.DateTime : 'datetime'
                }
                unainfo["type"] = types[ type(objcolumn) ]
            unainfo["name"] = name
            unainfo['primary'] = objcolumn.__dict__['_primary'] if "_primary" in objcolumn.__dict__ else False
            unainfo["null"] = objcolumn.__dict__['_variable_kwargs']["allow_none"] if "allow_none" in objcolumn.__dict__['_variable_kwargs'] else True
            unainfo["default"] = objcolumn.__dict__['_variable_kwargs']["value_factory"] if objcolumn.__dict__['_variable_kwargs']["value_factory"] == "Undef" else None
            resultado[objcolumn]=unainfo
        return resultado

    def getClassAttributesValues(self,obj):
        '''
        obtiene los valores de el obj
        @param obj:a obj de type 
        @return: a list of values
        '''
        if isinstance(obj, self.CLASS):
            return [obj.__getattribute__(p) for p in self.getClassAttributes()]
        else:
            raise Exception("no se pudo obtener los valores")
            
    def _obtenerNombreReference(self, reference):
        for elem in  reference.__dict__["_cls"].__dict__:
            if reference.__dict__["_cls"].__dict__[elem] is reference:
                return elem
    
    def getDataObject(self,obj,columns):
        '''
        obtiene y devuelve una lista de los datos obtenidos a partir de las
        columnas y de los datos que maneja
        @param obj:objeto instancia a extrer ex:unCliente
        @param columns:storm columns :ex:[Cliente.ide,Cliente.nombres]
        @return: lista de dic: [{"ide":1},{"nombres":nombrecliente}]
        '''
        if isinstance(obj, self.CLASS):
            listpropiertisvalues = []
            for propiedad in columns:
                nombreatributo = self.obtenerNombreAtributo(propiedad)
                listpropiertisvalues.append({nombreatributo:obj.__getattribute__(nombreatributo)})
            return listpropiertisvalues
        else:
            raise Exception("no se pudo obtener los valores debido a que no es una instancia correcta")
        
    def propertyToColumn(self,propiedad):
        '''
        a partir de un propierty devuelve el column correspondiente
        @param propiedad:la propyerty
        '''
        nombreatributo = self._obtenerNombreProperty(propiedad)
        return self.CLASS.__dict__[nombreatributo]
     
    def obtenerNombreAtributo(self, property_reference):
        """
        Obtiene el nombre en string de un property/reference.
        """        
        if type(property_reference) == storm.references.Reference:
            return self._obtenerNombreReference(property_reference)
        else:
            return self._obtenerNombreProperty(property_reference)
        
#=======================================================================
# Generic Methods  
#=======================================================================

    def add(self,*params):
        '''
        Crea y agrega un objeto al almacen
        @param *params: los parametros que recibe el init de self.CLASS
        @return: true o false, dependiendo si se completo la operacion
        '''
        try:
            obj = self.CLASS(*params)
            self.almacen.add(obj)
            self.almacen.flush()
            self.almacen.commit()
            return True
        except Exception, e:
            print 'BaseManager.add() : ',self.CLASS, e
            return False
        
    def delete(self,obj):
        '''
        borra un objeto de la bd y de la ram
        @param obj:un objeto del tipo self.CLASS
        '''
        if isinstance(obj, self.CLASS):
            self.almacen.remove(obj)#where o is the object representing the row you want to remove
            del obj#lo sacamos de la ram
            self.almacen.commit()
            return True
        
    def getall(self):
        '''
        obtiene todos los objetos de este manager
        @return: lista de objs
        '''
        return [obj for obj in self.almacen.find(self.CLASS)]

    def get(self,nombre):
        '''
        obtiene los objetos donde "nombre" coincide con self.searchname
        @param nombre:str o int
        @return: list of obj
        '''
        if not self.searchname:
            self.searchname = self.CLASS.nombre
        return self.searchBy(self.searchname,nombre)

    def searchBy(self,column,nombre):
        '''
        hace una busqueda e el atributo column por el valor nombre
        @param column:a storm column
        @param nombre:str o int
        @return: lista de objetos
        '''
        if type(column) == storm.references.Reference:
            objs = self.getall()
            name = self._obtenerNombreReference(column)      
            return [obj for obj in objs if nombre in obj.__getattribute__(name).__str__()]
        if nombre != "":
            try:
                return [obj for obj in self.almacen.find(self.CLASS,column.like(unicode(u"%"+nombre+u"%")))]
            except TypeError:
                try:
                    return [obj for obj in self.almacen.find(self.CLASS,column == int(nombre))]
                except Exception, e:
                    print e
                    return []
        else:
            return self.getall()
        
    def getClassIdString(self):
        atributes_info = self.getClassAttributesInfo().values()
        return [ atributo['name'] for atributo in atributes_info if atributo['primary'] == True][0]
    
    
