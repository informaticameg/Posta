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
from PyQt4 import QtCore, QtGui, uic


class CombinacionesDeTeclas(QtGui.QDialog):

    def __init__(self, parent = None):
        self.parent = parent
        self.FILENAME = 'pos/combteclas.ui'
        QtGui.QDialog.__init__(self)
        UI_CONTENT = cStringIO.StringIO(self.parent.uis[self.FILENAME])
        uic.loadUi(UI_CONTENT, self)
        self.__centerOnScreen()

        self.setWindowTitle("Combinaciones de teclas")
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))


def main():
    app = QtGui.QApplication(sys.argv)
    window = CombinacionesDeTeclas()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
