from application.view.inventory.inventory import API_inventories
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app as app

from application.controller.warehouse_api import WarehousesAPI, WarehouseAPI, WareInventAPI
from application.controller.inventory_api import InventoriesAPI

API_warehouses = WarehousesAPI()
API_warehouse = WarehouseAPI()
API_inventories = InventoriesAPI()
API_wareinvent = WareInventAPI()

# Blueprint Configuration
warehouse_bp = Blueprint(
    'warehouse_bp', __name__,
    template_folder='templates',
    url_prefix='/warehouses'
)


@warehouse_bp.route('/', methods=['GET'])
def warehouses():
    """Homepage."""
    
    warehouses = API_warehouses.get()
    return render_template(
        'warehouses.html',
        warehouses = warehouses
    )
    
@warehouse_bp.route('/new', methods=['GET'])
def warehouses_new():
    return render_template(
        'warehouses_new.html',
    )

@warehouse_bp.route('/new/submit', methods=['POST'])
def Warehouse_new_submit():
    data = request.form
    return_message = API_warehouses.post(data)
    flash(return_message)
    return redirect(url_for('warehouse_bp.warehouses'))

@warehouse_bp.route('/<id>/edit', methods=['GET'])
def Warehouse_edit(id):
    warehouse= API_warehouse.get(id)
    return render_template(
        'warehouse_edit.html',
        warehouse=warehouse,
    )


@warehouse_bp.route('/edit/submit', methods=['POST'])
def Warehouse_edit_submit():
    data = request.form
    API_warehouse.put(data['id'], data)
    return redirect(url_for('warehouse_bp.warehouses'))

@warehouse_bp.route('/<id>/delete', methods=['GET'])
def Warehouse_delete(id):
    warehouse = API_warehouse.delete(id)
    return redirect(url_for('warehouse_bp.warehouses'))
    
    
    
@warehouse_bp.route('/<id>', methods=['GET'])
def warehouse(id):
    #update the current_load
    API_warehouse.get(id)
    
    #get full info of inventories hold by warehouse
    warehouse_info = API_wareinvent.get(id)
    
    #get all available inventories
    all_inventories = API_inventories.get()
    return render_template(
        'warehouse.html',
        warehouse_info = warehouse_info,
        all_inventories = all_inventories
        
    )
    
    
@warehouse_bp.route('/<id>/remove', methods=['POST'])
def Warehouse_remove_inventory(id):
    data = request.form
    print(data)
    API_wareinvent.put(data['w_id'], data['i_id'], int(data['remove'])*-1)
    return redirect(url_for('warehouse_bp.warehouse', id=data['w_id']))

@warehouse_bp.route('/<id>/add', methods=['POST'])
def Warehouse_add_inventory(id):
    data = request.form
    print(data)
    API_wareinvent.put(data['w_id'], data['i_id'], data['add'])
    return redirect(url_for('warehouse_bp.warehouse', id=data['w_id']))
