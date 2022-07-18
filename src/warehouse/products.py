from utils import valid_key, InvalidItem, ItemExists, InsufficientInventory, ItemMissing

class Products:
    @staticmethod
    def initialize_db(mongo):
        Products.collection = mongo.db.products

    @staticmethod
    def add_products(products):
        products = products['products']
        for i, p in enumerate(products):
            try:
                Products.validate_product(p)
            except InvalidItem as error:
                raise InvalidItem(error.message + " at index " + str(i))

        for p in products:
            data = Products.get_product(p['name'])
            if data is None:
                Products.add_product(p)
            else:
                Products.update_product(p['name'], p)

    @staticmethod
    def add_product(product):
        Products.validate_product(product)
        data = Products.get_product(product['name'])
        if data is not None:
            raise ItemExists
        Products.collection.insert_one(product)

    @staticmethod
    def delete_product(name):
        Products.collection.delete_one({'name': name})
        return True

    @staticmethod
    def update_product(name, product):
        Products.validate_product(product)
        result = Products.collection.update_one(
            {"name": name},
            {'$set': product})
        data = Products.get_product(name)
        if data is None:
            raise ItemMissing
        return True

    @staticmethod
    def get_product(name, get_quantity = False):
        if get_quantity:
            product = Products.get_all_product(name)
            if len(product) > 0:
                return product[0]
            return None
        return Products.collection.find_one(
            {"name": name},
            {'_id': False}
        )

    @staticmethod
    def get_all_product(name = None):
        pipeline = [
            {
                "$lookup": {
                    "from": "inventory",
                    "localField": "contain_articles.art_id",
                    "foreignField": "art_id",
                    "as": "art_id_map"
                }
            },
            {
                "$project": {
                    "name": 1,
                    "contain_articles": 1,
                    "inventory": {
                        "$map": {
                            "input": {"$range": [0, { "$size": "$contain_articles"}]},
                            "as": "idx",
                            "in": {
                                "$mergeObjects": [
                                    {"$arrayElemAt": ["$contain_articles","$$idx" ]},
                                    {"$arrayElemAt": [ "$art_id_map","$$idx" ]}
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$project": {
                    "name": 1,
                    "contain_articles": 1,
                    "inventory": 1,
                    "quantity_all": {
                        "$map": {
                            "input": {"$range": [0, {"$size": "$inventory"}]},
                            "as": "idx",
                            "in": {
                                "$divide": [
                                    {"$arrayElemAt": ["$inventory.stock","$$idx" ]},
                                    {"$arrayElemAt": ["$inventory.amount_of", "$$idx"]}
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "inventory.art_id": 1,
                    "inventory.amount_of": 1,
                    "inventory.name": 1,
                    "inventory.stock": 1,
                    "quantity": {"$trunc": { "$min": "$quantity_all" }}
                }
            }
        ]
        if name != None:
            pipeline.insert(0, { "$match": { "name": name } },)

        return list(Products.collection.aggregate(pipeline))

    @staticmethod
    def validate_product(p):
        if not valid_key(p, 'name', 'str'):
            raise InvalidItem("Invalid name of product")

        if not valid_key(p, 'contain_articles', 'list'):
            raise InvalidItem("Invalid contain_articles of product")

        for i, a in enumerate(p['contain_articles']):
            if not valid_key(a, 'art_id', 'str', True):
                raise InvalidItem("Invalid art_id in contain_articles of product")

            if not valid_key(a, 'amount_of', 'str', True) and not valid_key(a, 'amount_of', 'int'):
                raise InvalidItem("Invalid amount_of in contain_articles of product")

            p['contain_articles'][i]['amount_of'] = int(a['amount_of'])
            print(p['contain_articles'][i]['amount_of'] )