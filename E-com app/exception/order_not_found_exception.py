class OrderNotFoundException(Exception):
    def __init__(self, message="Order not found in the database"):
        self.message = message
        super().__init__(self.message)
