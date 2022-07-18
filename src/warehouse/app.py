import json
import traceback

from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from inventory import *
from products import *
from utils import (InsufficientInventory, InvalidItem, ItemExists, ItemMissing)
from warehouse import *

warehouse_app = Flask(__name__)
DB_BASE_URI = "mongodb://mongodb"
db_object = None

def connect_to_mongo(db_name):
    global db_object
    if db_object != None:
        return db_object
    warehouse_app.config["MONGO_URI"] = DB_BASE_URI + "/" + db_name
    db_object = PyMongo(warehouse_app)

    # Initialize warehouse
    Warehouse.initialize_db(db_object)
    return db_object

connect_to_mongo("warehouse")

########### Product related API Calls
@warehouse_app.route('/product_upload', methods=['POST'])
def product_upload():
    """
    Takes a list of product item as json and updates the database, the product
    exists then it is replaced
    Arguments:
        file: A json file
    Returns:
        JSON message
    """
    try:
        if request.method == 'POST':
            f = request.files['file']
            json_data = json.loads(f.read())
            Products.add_products(json_data)
            return jsonify({'ok': True, 'message': 'Products Uploaded'}), 200
        return jsonify({'ok': False, 'message': 'Invalid require method'}), 400

    except InvalidItem as err:
        return jsonify({
            'ok': False,
            'message': err.message}), 400
    except:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': True,
            'message': 'Internal Server Error'}), 500

@warehouse_app.route('/product', methods=['GET', 'POST', 'DELETE', 'PUT'])
def product():
    """
    GET: Return the product by name
    POST: Adds a new product if it does not exists in DB
    PUT: Update product if it exists in DB
    DELETE: Remove the product object from DB
    Arguments:
        name: name of product as string
        product: A json object with keys
    Returns:
        JSON message
    """
    try:
        name = request.args.get('name', None)
        product = None
        try:
            product = request.get_json()
        except Exception:
            pass

        # Exceute request
        if request.method == 'GET':
            data = Products.get_product(name)
            return jsonify(data), 200

        if request.method == 'POST':
            try:
                Products.add_product(product)
                return jsonify({
                    'ok': True,
                    'message': 'Product created successfully!'}), 200
            except ItemExists:
                return jsonify({
                    'ok': True,
                    'message': 'Product already exists!'}), 200

        if request.method == 'DELETE':
            Products.delete_product(name)
            return jsonify({
                'ok': True,
                'message': 'Product deleted successfully!'}), 200

        if request.method == 'PUT':
            try:
                Products.update_product(name, product)
            except ItemMissing:
                return jsonify({
                    'ok': True,
                    'message': 'Product does not exists!'}), 200

            return jsonify({
                'ok': True,
                'message': 'Product updated successfully!'}), 200

    except InvalidItem as err:
        return jsonify({
            'ok': False,
            'message': err.message}), 400

    except Exception:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': True,
            'message': 'Internal Server Error'}), 500

@warehouse_app.route('/product_all', methods=['GET'])
def product_all():
    """
    List all the products, along with the quanity
    Returns:
        JSON data
    """
    try:
        data = Products.get_all_product()
        print(data)
        return jsonify(data), 200
    except:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': True,
            'message': 'Internal Server Error'}), 500

@warehouse_app.route('/product_sell/<name>', methods=['GET'])
def product_sell(name):
    """
    Removes the amount of inventory required by the given product
    Returns:
        JSON response
    """
    try:
        Warehouse.sell_product(name)
        return jsonify({
            'ok': True,
            'message': 'Item sold successfully!'}), 200
    except ItemMissing:
        return jsonify({
            'ok': True,
            'message': 'Product does not exists!'}), 200
    except InsufficientInventory:
        return jsonify({
            'ok': True,
            'message': 'Insufficient Inventory!'}), 200
    except:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': True,
            'message': 'Internal Server Error'}), 500

########### Inventory related API Calls
@warehouse_app.route('/inventory_all', methods=['GET'])
def inventory_all():
    """
    List all the inventory item
    Returns:
        JSON data
    """
    try:
        data = Inventory.get_all_inventory_items()
        return jsonify(data), 200
    except:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': True,
            'message': 'Internal Server Error'}), 500

@warehouse_app.route('/inventory_upload', methods=['POST'])
def inventory_upload():
    """
    Takes a list of inventory item as json and updates the database, if the
    item exists in DB then stock is updated only i.e increased in its value
    Arguments:
        file: A json file
        replace_stock: True to replace orginal stock value otherwise increment
            it. False by default
    Returns:
        JSON message
    """
    try:
        if request.method == 'POST':
            f = request.files['file']
            replace_stock = request.form.get("replace_stock")
            if replace_stock == None:
                replace_stock = False
            elif replace_stock == "True" or replace_stock == "true":
                replace_stock = True

            json_data = json.loads(f.read())
            Inventory.add_inventory_items(json_data, replace_stock)
            return jsonify({'ok': True, 'message': 'Inventory Uploaded'}), 200
        return jsonify({'ok': False, 'message': 'Invalid require method'}), 400
    except:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': True,
            'message': 'Internalxxx Server Error ' + traceback.format_exc()}), 500

@warehouse_app.route('/inventory', methods=['GET', 'POST', 'DELETE', 'PUT'])
def inventory():
    """
    GET: Return the inventory item by name
    POST: Adds a new inventory item if it does not exists in DB
    PUT: Update inventory item if it exists in DB
    DELETE: Remove the inventory item object from DB
    Arguments:
        art_id: art_id id of item as string, required for GET, DELETE and PUT
        item: A json object with keys, required for POST and PUT
    Returns:
        JSON message
    """
    try:
        art_id = request.args.get('art_id', None)
        inventory_item = None
        try:
            inventory_item = request.get_json()
        except Exception:
            pass

        # Exceute request
        if request.method == 'GET':
            data = Inventory.get_inventory_item(art_id)
            return jsonify(data), 200

        if request.method == 'DELETE':
            Inventory.delete_inventory_item(art_id)
            return jsonify({
                'ok': True,
                'message': 'inventory item deleted successfully!'}), 200

        if request.method == 'PUT':
            Inventory.update_inventory_item(art_id, inventory_item)
            return jsonify({
                'ok': True,
                'message': 'inventory item updated successfully!'}), 200

        if request.method == 'POST':
            try:
                Inventory.add_inventory_item(inventory_item)
                return jsonify({
                    'ok': True,
                    'message': 'inventory item created successfully!'}), 200
            except ItemExists:
                return jsonify({
                    'ok': True,
                    'message': 'inventory item already exists!'}), 200

    except InvalidItem as err:
        return jsonify({
            'ok': False,
            'message': err.message}), 400

    except Exception as err:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': False,
            'message': "Internal Server Error"}), 500

@warehouse_app.route('/inventory_add_stock/<art_id>/<stock>', methods=['GET'])
def inventory_add_stock(art_id, stock):
    """
    GET: Add the stock to the given inventory item
    Arguments:
        art_id: id of inventory item as string
        stock: stock as numeric string
    Returns:
        JSON message
    """
    return inventory_add_or_remove(art_id, stock)

@warehouse_app.route('/inventory_remove_stock/<art_id>/<stock>', methods=['GET'])
def inventory_remove_stock(art_id, stock):
    """
    GET: Reduce the stock of the given inventory item
    Arguments:
        art_id: id of inventory item as string
        stock: stock as numeric string
    Returns:
        JSON message
    """
    return inventory_add_or_remove(art_id, "-" + stock)

def inventory_add_or_remove(art_id, stock):
    """
    A helper method for inventory_add_stock and inventory_remove_stock functions
    Arguments:
        name: name of inventory item as string
        stock: stock as numeric string
    Returns:
        JSON message
    """
    try:
        new_stock = Inventory.add_or_remove_stock(art_id, stock)
        return jsonify({
            'ok': True,
            'message': 'Inventory item stock changed to: ' + str(new_stock)}), 200

    except ItemMissing as err:
        return jsonify({
            'ok': False,
            'message': "No inventory item found with given id" + str(art_id)}), 400

    except InsufficientInventory as err:
        return jsonify({
            'ok': False,
            'message': "Not enough inventory to remove"}), 400

    except Exception as err:
        print("Error:")
        print(traceback.format_exc())
        return jsonify({
            'ok': False,
            'message': "Internal Server Error"}), 500

@warehouse_app.route('/clear_db', methods=['GET'])
def clear_db():
    Warehouse.clear_warehouse(db_object)

def create_app():
    warehouse_app.run(debug=True, port=80, host='0.0.0.0')
