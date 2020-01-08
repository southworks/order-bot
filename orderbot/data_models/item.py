class Item:
    def __init__(self, product_id: int = 0, description: str = None, item_id: id = 0, known_names: str = None):
        self.product_id = product_id
        self.description = description
        self.item_id = item_id
        self.known_names = known_names
