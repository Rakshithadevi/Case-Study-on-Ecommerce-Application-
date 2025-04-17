class CustomerNotFoundException(Exception):
    def __init__(self, message="Customer not found in the database"):
        self.message = message
        super().__init__(self.message)
