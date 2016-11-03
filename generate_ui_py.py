#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

_data_files = [
        ('', [r'acercade.ui']),
        (r'categoria',[r'categoria\admin.ui', r'categoria\agregar.ui']),
        (r'entrada',[r'entrada\entrada.ui']),
        (r'GUI',[r'GUI\all_modules.ui']),
        (r'inventario',[r'inventario\admin.ui',
            r'inventario\agregarinventario.ui',
            r'inventario\actualizarprecios.ui',
            r'inventario\impexp.ui']),
        (r'plasta',[r'plasta\gui\uis\admin.ui', r'plasta\gui\uis\buscador.ui']),
        (r'pos',[r'pos\artcomun.ui',
            r'pos\cobrar.ui',
            r'pos\cobrar_con_cliente.ui',
            r'pos\combteclas.ui',
            r'pos\pos.ui',
            r'pos\varios.ui',
            r'pos\ventas.ui']),
        (r'producto',[r'producto\admin.ui', r'producto\agregar.ui']),
        (r'resumen',[r'resumen\admin.ui']),
        (r'salida',[r'salida\salida.ui']),
        (r'venta',[r'venta\admin.ui', r'venta\agregar.ui']),
        (r'setting',[r'setting\gui.ui'])
    ]

uiContents = {}

for folder, uis in _data_files:
    for _ui in uis:
        if os.name == 'posix':
            _ui = _ui.replace('\\','/')
        contenUi = open(_ui, 'r').read().replace('\n','')
        uiContents[_ui.replace('\\','/')] = contenUi

uiContents = str(uiContents).replace("', '", "',\n'")
contentPy = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
uis = %s """ % uiContents
res = open('uis.py', 'w').write(contentPy)
print 'ok...'