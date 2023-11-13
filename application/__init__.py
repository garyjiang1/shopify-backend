from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api

db = SQLAlchemy()
migrate = Migrate()
api = Api()

### Important: Need to import after initialize db instance to avoid circular import 
from application.model import Model
from application.controller.warehouse_api import WarehousesAPI, WarehouseAPI, WareInventAPI
from application.controller.inventory_api import InventoriesAPI, InventoryAPI


def init_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    print(app.config['FLASK_ENV'])
    
    #Initialize Plugins
    db.init_app(app)
    migrate.init_app(app)
    api.add_resource(WarehousesAPI, '/api/warehouses')
    api.add_resource(WarehouseAPI, '/api/warehouse/<id>')
    api.add_resource(InventoriesAPI, '/api/inventories')
    api.add_resource(InventoryAPI, '/api/inventory')
    api.add_resource(WareInventAPI, '/api/wareinvent')
    api.init_app(app)
    model = Model(app)
    
    
    with app.app_context():
        #Import routes
        from .view.home import home
        from .view.warehouse import warehouse
        from .view.inventory import inventory
        
        #Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(warehouse.warehouse_bp)
        app.register_blueprint(inventory.inventory_bp)
        
        #Register API resources 
        
        
        migrate.init_app(app, db)
    
        return app 