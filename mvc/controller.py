#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import * #@UnusedWildImport
from tools import pathtools

class Controller :
    
    def __init__(self):
        self.DATABASE = None
        self.almacen = None
        self.dbExist = False
        self.openConnection()
        self.pathDB = ''
        
    def openConnection(self):
        print 'abriendo conexion...'
        self.DATABASE = None
        self.almacen = None
        
        self.checkDBExists()
        self.DATABASE = create_database('sqlite:' + self.pathDB)
        self.almacen = Store(self.DATABASE)
        
    def closeConnection(self):
        print 'cerrando conexion...'
        self.almacen.commit()
        self.almacen.close()
        
    def checkDBExists(self):
        import os.path, os
        rf = pathtools.getPathProgramFolder()
        db_folder = pathtools.convertPath(rf + '/data')
        db_file = pathtools.convertPath(db_folder + '/posta.data')
        self.pathDB = db_file
        if not os.path.exists(db_folder):
            os.mkdir(db_folder)
        
        self.dbExist = os.path.exists(db_file)
        if not self.dbExist:
            _f = open(db_file, 'w')
            _f.write('')
            _f.close()