import unittest
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from entity.Product import Product
from entity.Customer import Customer
from exception.customer_not_found_exception import CustomerNotFoundException
from exception.product_not_found_exception import ProductNotFoundException
import random
import mysql.connector


class TestOrderProcessorRepositoryImpl(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = OrderProcessorRepositoryImpl()

        # Create a test customer
        cls.customer = Customer(
            name="UnitTest User",
            email=f"testuser_{random.randint(1000, 9999)}@test.com",
            password="test123"
        )
        cls.repo.create_customer(cls.customer)
        cls.test_customer_id = cls.customer.get_customer_id()

        # Create a test product
        cls.product = Product(
            name="Test Product",
            price=99.99,
            description="Unit test product",
            stock_quantity=50
        )
        cls.repo.create_product(cls.product)
        cls.test_product_ids = [cls.product.get_product_id()]
        cls.test_order_ids = []

    def test_1_create_product_success(self):
        new_product = Product(
            name="New Test Product",
            price=49.99,
            description="Another test product",
            stock_quantity=30
        )
        result = self.repo.create_product(new_product)
        self.assertTrue(result)
        self.assertIsNotNone(new_product.get_product_id())

        # Append using class-level reference
        type(self).test_product_ids.append(new_product.get_product_id())

    def test_2_add_to_cart_success(self):
        result = self.repo.add_to_cart(self.customer, self.product, quantity=2)
        self.assertTrue(result)

    def test_3_place_order_success(self):
        cart_items = [{"product": self.product, "quantity": 2}]
        result = self.repo.place_order(self.customer, cart_items, "123 Test Lane")
        self.assertTrue(result)

        # Fetch latest order ID for cleanup
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='rakshi430',        # ✅ Use your actual DB password
            database='ecomm_db'          # ✅ Use your actual DB name
        )
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(order_id) FROM orders WHERE customer_id = %s", (self.test_customer_id,))
        order_id = cursor.fetchone()[0]
        if order_id:
            type(self).test_order_ids.append(order_id)
        cursor.close()
        conn.close()

    def test_4_customer_not_found_exception(self):
        fake_customer = Customer(name="Fake", email="fake@test.com", password="fake123")
        fake_customer.set_customer_id(99999)
        with self.assertRaises(CustomerNotFoundException):
            self.repo.add_to_cart(fake_customer, self.product, quantity=1)

    def test_5_product_not_found_exception(self):
        fake_product = Product(name="Ghost", price=0.0, description="Ghost", stock_quantity=0)
        fake_product.set_product_id(99999)
        with self.assertRaises(ProductNotFoundException):
            self.repo.add_to_cart(self.customer, fake_product, quantity=1)

    @classmethod
    def tearDownClass(cls):
        print("Running tearDownClass...")
        print("Order IDs:", cls.test_order_ids)
        print("Product IDs:", cls.test_product_ids)
        print("Customer ID:", cls.test_customer_id)

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='rakshi430',  # ✅ Your actual password
                database='ecomm_db'
            )
            cursor = conn.cursor()

            # Delete order items and orders
            for order_id in cls.test_order_ids:
                cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
                cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))

            # Delete from cart
            for product_id in cls.test_product_ids:
                cursor.execute("DELETE FROM cart WHERE customer_id = %s AND product_id = %s",
                               (cls.test_customer_id, product_id))

            # Delete products
            for product_id in cls.test_product_ids:
                cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))  # ✅ FIXED

            # Delete customer
            cursor.execute("DELETE FROM customers WHERE customer_id = %s", (cls.test_customer_id,))  # ✅ FIXED

            conn.commit()
            cursor.close()
            conn.close()
            print("Test data cleaned up successfully.")
        except Exception as e:
            print("Error in tearDownClass:", e)


if __name__ == "__main__":
    unittest.main()
