from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app as app
import requests
from application.controller.inventory_api import InventoriesAPI, InventoryAPI


API_inventories = InventoriesAPI()
API_inventory = InventoryAPI()

# Blueprint Configuration
inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='templates',
    url_prefix='/inventories'
)


@inventory_bp.route('/', methods=['GET'])
def inventories_all():
    all_inventories = API_inventories.get()
    return render_template(
        'inventories.html',
        all_inventories=all_inventories,
    )

@inventory_bp.route('/new', methods=['GET'])
def inventories_new():
    return render_template(
        'inventories_new.html',
    )

@inventory_bp.route('/new/submit', methods=['POST'])
def Inventory_new_submit():
    data = request.form
    return_message = API_inventories.post(data)
    flash(return_message)
    return redirect(url_for('inventory_bp.inventories_all'))


@inventory_bp.route('/<id>/edit', methods=['GET'])
def Inventory_edit(id):
    inventory = API_inventory.get(id)
    return render_template(
        'inventory_edit.html',
        inventory=inventory,
    )
    
@inventory_bp.route('/edit/submit', methods=['POST'])
def Inventory_edit_submit():
    data = request.form
    API_inventory.put(data['id'], data)
    return redirect(url_for('inventory_bp.inventories_all'))

@inventory_bp.route('/<id>/delete', methods=['GET'])
def Inventory_delete(id):
    inventory = API_inventory.delete(id)
    return redirect(url_for('inventory_bp.inventories_all'))