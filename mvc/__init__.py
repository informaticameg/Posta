from mvc.controller import Controller
from mvc.model import Models
from mvc.view import View


class Main :
    
    def __init__(self):
        self.controller = Controller()
        self.models = Models( self.controller )
        self.view = View( self.models )

        
