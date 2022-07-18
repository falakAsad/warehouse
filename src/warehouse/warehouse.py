from inventory import *
from products import *
from utils import *

class Warehouse:

    @staticmethod
    def initialize_db(mongo):
        Products.initialize_db(mongo)
        Inventory.initialize_db(mongo)

    @staticmethod
    def sell_product(name):
        # Remove values from inventory
        product = Products.get_product(name, True)
        if product == None:
            raise ItemMissing
        if product['quantity'] > 0:
            for art_required in product['inventory']:
                Inventory.add_or_remove_stock(art_required['art_id'], -abs(art_required['amount_of']))
        else:
            raise InsufficientInventory
        return True

    def clear_warehouse(mongo):
        mongo.db.products.drop()
        mongo.db.inventory.drop()
