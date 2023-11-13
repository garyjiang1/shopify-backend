from flask_restful import Resource
from flask import Response, request
from datetime import datetime
import json

from application import db
from application.model.model import Warehouse, Has, Inventory

class WarehousesAPI(Resource):
    def get(self):
        warehouses = Warehouse.query.order_by(Warehouse.id).all()

        return [{'id': warehouse.id, 
                 'name': warehouse.name, 
                 'address': warehouse.address,
                 'capacity':warehouse.capacity,
                 'current_load':warehouse.current_load,
                 'created_time': str(warehouse.created_time),
                 'updated_time': str(warehouse.updated_time)} for warehouse in warehouses]

    def post(self, data):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        if data['capacity'] and int(data['capacity']) > 0:
            new_warehouse = Warehouse(data['name'], data['address'], data['capacity'], dt_string, 0)
        else:
            return "capacity must larger than 0"
        db.session.add(new_warehouse)
        db.session.commit()
        return "suceess"


class WarehouseAPI(Resource):
    def get(self, id):
        warehouse = Warehouse.query.filter_by(id = id).first()
        
        #using group by on Has table to fetch all current load 
        #load_info = db.session.query(db.func.sum(Has.amount)).filter_by(w_id=id).group_by(Has.w_id).first()
        load_info = db.session.query((Has.amount)).filter_by(w_id=id).all()
        
        if load_info:
            print(load_info)
            load_info = sum([int(num[0]) for num in load_info])
            warehouse.current_load = load_info
        else:
            warehouse.current_load = 0
        db.session.commit()
        return warehouse
    

    
    def put(self, id, data):
        
        warehouse = Warehouse.query.filter_by(id=id).first()
        if int(data['capacity']) < warehouse.current_load:
            return "Cannot set capacity lower than current load."
        warehouse.name = data['name']
        warehouse.address = data['address']
        warehouse.capacity = data['capacity']

        warehouse.updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        
        return
    

        
    def delete(self, id):
        warehouse = Warehouse.query.filter_by(id = id).first()
        db.session.delete(warehouse)
        db.session.commit()

class WareInventAPI(Resource):
    def get(self, id):
        warehouse = Warehouse.query.filter_by(id = id).outerjoin(Has).outerjoin(Inventory).with_entities(
        Warehouse.id, Warehouse.address, Warehouse.name, Warehouse.capacity, Warehouse.current_load, Inventory.id, Inventory.name,  Inventory.price,Inventory.amount, Inventory.not_allocated, Has.amount).all()
        
        return warehouse
    
    
    def put(self, w_id, i_id, add_amount):
        add_amount = int(add_amount)
        has_item = Has.query.filter_by(w_id=w_id, i_id=i_id).first()
        inventory = Inventory.query.filter_by(id=i_id).first()
        
        print(has_item)
        if has_item:
            has_item.amount = int(has_item.amount)
            if has_item.amount + add_amount > 0:
                inventory.not_allocated -= add_amount
                has_item.amount += add_amount
            else:
                inventory.not_allocated += has_item.amount
                db.session.delete(has_item)
            db.session.commit()
            return "amount updated"

        if add_amount <= inventory.not_allocated:
            new_item = Has(w_id=w_id, i_id=i_id, amount=add_amount)
            inventory.not_allocated -= add_amount
            db.session.add(new_item)
            db.session.commit()
            return "added new inventory to warehouse"
        else:
            return "Not enough inventory"
    #add new inventory to warehouse (add)
    # def post(self, data):
    #     wareinvent = Warehouse.query.filter_by(id=data['w_id']).join(has).filter_by(i_id=data['i_id']).first()
    #     print(wareinvent)
    #     if wareinvent:
    #         wareinvent.amount += data.add
    #         db.session.commit()
    #         return "amount added to existing warehouse inventory pair"
    #     #new_wareinvent = has(data['w_id'], data['i_id'], data['add'])
    #     warehouse = Warehouse.query.filter_by(id=data['w_id'])
    #     inventory = Inventory.query.filter_by(id=data['i_id'])
    #     inventory.amount = data.add
    #     warehouse.holds.append(inventory)
    #     #db.session.add(new_wareinvent)
    #     db.session.commit()
    #     return "New warehouse inventory pair created"
    
    # # Modify existing inventory in the warehouse (remove)
    # def put(self, data):
    #     wareinvent = Warehouse.query.filter_by(id=data['w_id']).join(has).filter_by(i_id=data['i_id'])
    #     if wareinvent:
    #         if wareinvent.amount >= data['remove']:
    #             wareinvent.amount -= data['remove']
    #         else:
    #             wareinvent.amount = 0
    #         db.session.commit()
    #         return "Inventory removed"
    #     return "Inventory Warehouse pair not found"