#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from salida.add import AddSalida
from PyQt4 import QtCore, QtGui

class SalidaGUI(BaseGUI):
    
    def __init__(self, parent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)
        self.DialogAddClass  = AddSalida
        self._operaciones_de_inicio()
