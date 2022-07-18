
class InvalidItem(Exception):
    message = ""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ItemExists(Exception):
    pass

class ItemMissing(Exception):
    pass

class InsufficientInventory(Exception):
    pass

def valid_key(p, key, expectedType, isNumeric = False):
    if key not in p or p[key] is None or type(p[key]).__name__ != expectedType:
        return False

    if isNumeric is True and not p[key].isnumeric():
        return False

    return True
