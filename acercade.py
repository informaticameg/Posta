#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Informática MEG <contacto@informaticameg.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os, sys, cStringIO
from PyQt4 import QtGui, uic
import GUI.images_rc #@UnusedImport

class AcercaDe(QtGui.QMainWindow):
    
    def __init__(self, parent, setting):
        self.parent = parent
        FILENAME = 'acercade.ui'
        QtGui.QMainWindow.__init__(self)
        UI_CONTENT = cStringIO.StringIO(self.parent.uis[FILENAME])
        uic.loadUi(UI_CONTENT, self)
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png')) 
        self.__centerOnScreen()

        self.lbVersion.setText('%s.0' % setting.version)
                
    def __centerOnScreen (self):
        """Centers the window on the screen."""
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))      
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = AcercaDe()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    
    main()
