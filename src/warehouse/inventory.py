from utils import valid_key, InvalidItem, ItemExists, InsufficientInventory, ItemMissing

class Inventory:
    @staticmethod
    def get_inventory_item(art_id):
        return Inventory.collection.find_one(
            {"art_id": art_id},
            {'_id': False}
        )

    @staticmethod
    def initialize_db(mongo):
        Inventory.collection = mongo.db.inventory

    @staticmethod
    def get_all_inventory_items():
        return list(Inventory.collection.find({}, {'_id': False}))

    @staticmethod
    def add_inventory_item(item):
        Inventory.validate_inventory_item(item)
        data = Inventory.get_inventory_item(item['art_id'])
        if data is not None:
            raise ItemExists
        Inventory.collection.insert_one(item)

    @staticmethod
    def add_inventory_items(items, replace_stocks = False):
        items = items['inventory']
        for i, item in enumerate(items):
            try:
                Inventory.validate_inventory_item(item)
            except InvalidItem as error:
                raise InvalidItem(error.message + " at index " + str(i))

        for i, item in enumerate(items):
            data = Inventory.get_inventory_item(item['art_id'])
            if data is None:
                Inventory.add_inventory_item(item)
            else:
                if replace_stocks == True:
                    Inventory.update_inventory_item(item['art_id'], item)
                else:
                    item['stock'] = str(data['stock'] + item['stock'])
                    Inventory.update_inventory_item(item['art_id'], item)

    @staticmethod
    def delete_inventory_item(art_id):
        Inventory.collection.delete_one({'art_id': art_id})
        return True

    @staticmethod
    def update_inventory_item(art_id, item):
        Inventory.validate_inventory_item(item)
        Inventory.collection.update_one(
            {"art_id": art_id},
            {'$set': item})
        return True

    @staticmethod
    def update_inventory_stock(art_id, stock):
        Inventory.collection.update_one(
            {"art_id": art_id},
            {'$set': {"stock": stock}})
        return True

    @staticmethod
    def add_or_remove_stock(art_id, stock):
        data = Inventory.get_inventory_item(art_id)
        if data == None:
            raise ItemMissing

        initial_stock = data['stock']
        data['stock'] = initial_stock + int(stock)

        if data['stock'] < 0:
            raise InsufficientInventory

        Inventory.update_inventory_item(art_id, data)
        return data['stock']

    @staticmethod
    def validate_inventory_item(item):
        if not valid_key(item, 'name', 'str'):
            raise InvalidItem("Invalid name of inventory item")

        if not valid_key(item, 'art_id', 'str', True):
            raise InvalidItem("Invalid art_id of inventory item")

        if not valid_key(item, 'stock', 'str', True) and not valid_key(item, 'stock', 'int'):
            raise InvalidItem("Invalid stock of inventory item")

        item['stock'] = int(item['stock'])

