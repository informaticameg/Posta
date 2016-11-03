#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from entrada.add import AddEntrada
from PyQt4 import QtCore, QtGui

class EntradaGUI(BaseGUI):
    
    def __init__(self, parent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)
        self.DialogAddClass  = AddEntrada
        self._operaciones_de_inicio()
