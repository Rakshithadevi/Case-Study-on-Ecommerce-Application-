from abc import ABC, abstractmethod
from typing import List, Dict
from entity.Admin import Admin
from entity.Customer import Customer
from entity.Product import Product
from entity.Order import Order


class OrderProcessorRepository(ABC):

    @abstractmethod
    def create_product(self, product: Product) -> bool:
        pass

    @abstractmethod
    def create_customer(self, customer: Customer) -> bool:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int) -> bool:
        pass

    @abstractmethod
    def add_to_cart(self, customer: Customer, product: Product, quantity: int) -> bool:
        pass

    @abstractmethod
    def remove_from_cart(self, customer: Customer, product: Product) -> bool:
        pass

    @abstractmethod
    def get_all_from_cart(self, customer_id: int) -> List[dict]:
        pass

    @abstractmethod
    def place_order(self, customer: Customer, cart_items: list, shipping_address: str) -> bool:
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_id: int) -> list:
        pass

    @abstractmethod
    def create_admin(self, admin) -> bool:
        pass

    @abstractmethod
    def view_all_customers(self) -> List[Customer]:
        pass

    @abstractmethod
    def view_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def view_customer_orders(self, customer_id: int) -> List[Order]:
        pass

    @abstractmethod
    def get_customer_by_email(self, email: str) -> Customer:
        pass

    @abstractmethod
    def cancel_order(self, order_id: int) -> bool:
        pass

    @abstractmethod
    def login_admin(self, name: str, password: str) -> bool:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id):
        pass