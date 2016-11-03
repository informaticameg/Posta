from plasta.logic.manager import BaseManager
from setting import Setting

class SettingManager( BaseManager ):

    def __init__(self, store, reset = False ):
        BaseManager.__init__(self, store, reset)
        self.CLASS = Setting
        self._operaciones_de_inicio()

        if reset:
          self.add(u'1.3')

    def get(self):
      r = self.getall()
      return r[0] if len(r) > 0 else None

    def updateVersion(self, value):
      setting = self.get()
      setting.__setattr__('version', unicode(value))
      self.almacen.commit()