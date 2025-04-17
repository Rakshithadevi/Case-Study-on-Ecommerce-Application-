class OrderItem:
    def __init__(self, order_item_id=None, order_id=None, product_id=None, quantity=None, price=None):
        self.__order_item_id = order_item_id
        self.__order_id = order_id
        self.__product_id = product_id
        self.__quantity = quantity
        self.__price = price  # Price of the product in the order

    # Getters
    def get_order_item_id(self):
        return self.__order_item_id

    def get_order_id(self):
        return self.__order_id

    def get_product_id(self):
        return self.__product_id

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    # Setters
    def set_order_item_id(self, order_item_id):
        self.__order_item_id = order_item_id

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_price(self, price):
        self.__price = price

    # Method to calculate total price for this order item
    def get_total_price(self):
        return self.__price * self.__quantity if self.__price and self.__quantity else 0
