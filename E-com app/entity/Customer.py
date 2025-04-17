class Customer:
    def __init__(self, customer_id=None, name=None, email=None, password=None):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__password = password

    # Getters
    def get_customer_id(self):
        return self.__customer_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    # Setters
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__password = password
