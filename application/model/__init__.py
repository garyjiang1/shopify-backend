from application.model.model import Warehouse, Inventory

class Model:
    def __init__(self, app=None):
        if app != None:
            self.init_app(app)
        
    def init_app(self, app):
        app.model = self

        self.Warehouse = Warehouse
        self.Inventory = Inventory
