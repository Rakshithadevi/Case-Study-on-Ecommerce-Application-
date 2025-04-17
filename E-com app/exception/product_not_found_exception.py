class ProductNotFoundException(Exception):
    def __init__(self, message="Product not found in the database"):
        self.message = message
        super().__init__(self.message)
