#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *

class Setting (object):
    
    __storm_table__ = "Setting"

    ide = Int(primary = True)
    version = Unicode()
    vRemoto = Unicode()
    
    def __init__(self, version):
        self.version = version
        self.vRemoto = u'0'