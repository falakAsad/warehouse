
from utils import *
from inventory import *
from products import *

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
            for art_required in product['contain_articles']:
                Inventory.add_or_remove_stock(art_required['art_id'], -abs(art_required['amount_of']))
        else:
            raise InsufficientInventory
        # inventory_to_remove = { art['art_id'] : art['amount_of'] for art in product["contain_articles"] }
        # updated_stock_map = Inventory.remove_inventory(inventory_to_remove)
        # for art_id in updated_stock_map:
        #     self.update_inventory_stock(art_id, updated_stock_map[art_id])
        return True
