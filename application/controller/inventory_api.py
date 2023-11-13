
from flask_restful import Resource
from flask import Response, request
from datetime import datetime
import json

from application import db
from application.model.model import Inventory, Has

class InventoriesAPI(Resource):
    def get(self):
        Inventories = Inventory.query.order_by(Inventory.id).all()
        print(Inventories)

        return [{'id': inventory.id, 
                 'name': inventory.name, 
                 'price':inventory.price,
                 'amount': inventory.amount,
                 'not_allocated': inventory.not_allocated,
                 'updated_time': inventory.updated_time} for inventory in Inventories]

    def post(self, data):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        
        if data['price'] and data['amount'] and int(data['price']) > 0 and int(data['amount']) > 0:
            new_inventory = Inventory(data['name'], data['price'], data['amount'], dt_string)
        else:
            return "price and amount cannot be smaller than zero"
        db.session.add(new_inventory)
        db.session.commit()
        return "success"


class InventoryAPI(Resource):
    def get(self, id):
        inventory = Inventory.query.filter_by(id = id).first()
        return inventory
    
    def put(self, id, data):
        inventory = Inventory.query.filter_by(id = id).first()
        old_amount = inventory.amount
        print("old amount", old_amount)
        allocated = inventory.amount -inventory.not_allocated
        
        #Handle event when new amount is less than amount already allocated to warehouse
        if int(data['amount']) < allocated:
            return "New amount is less than amount allocated"
        
        inventory.name = data['name']
        inventory.price = float(data['price'])
            
        inventory.amount = int(data['amount'])
        inventory.not_allocated += (inventory.amount-old_amount)
        print("old amount", old_amount)
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        inventory.updated_time = dt_string
        db.session.commit()
        return "success"
    
    def delete(self, id):
        inventory = Inventory.query.filter_by(id = id).first()
        db.session.delete(inventory)
        db.session.commit()
        
    
    