from dao.OrderProcessorRepository import OrderProcessorRepository
from entity.Customer import Customer
from entity.Product import Product
from util.db_connection import DBConnection
from exception.customer_not_found_exception import CustomerNotFoundException
from exception.product_not_found_exception import ProductNotFoundException
from exception.order_not_found_exception import OrderNotFoundException


class OrderProcessorRepositoryImpl(OrderProcessorRepository):

    def create_product(self, product: Product) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO products (name, price, description, stockQuantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (
                product.get_name(),
                product.get_price(),
                product.get_description(),
                product.get_stock_quantity()
            ))
            product.set_product_id(cursor.lastrowid)
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error creating product: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def create_customer(self, customer: Customer) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (
                customer.get_name(),
                customer.get_email(),
                customer.get_password()
            ))
            customer.set_customer_id(cursor.lastrowid)
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error creating customer: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def delete_product(self, product_id: int) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            if cursor.fetchone() is None:
                raise ProductNotFoundException(f"Product with ID {product_id} not found.")

            query = "DELETE FROM products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            conn.commit()
            success = cursor.rowcount > 0
        except ProductNotFoundException as e:
            print(e)
            raise
        except Exception as e:
            print(f"Error deleting product: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def delete_customer(self, customer_id: int) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if cursor.fetchone() is None:
                raise CustomerNotFoundException(f"Customer with ID {customer_id} not found.")

            query = "DELETE FROM customers WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            conn.commit()
            success = cursor.rowcount > 0
        except CustomerNotFoundException as e:
            print(e)
            raise
        except Exception as e:
            print(f"Error deleting customer: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def add_to_cart(self, customer: Customer, product: Product, quantity: int) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer.get_customer_id(),))
            if cursor.fetchone() is None:
                raise CustomerNotFoundException(f"Customer with ID {customer.get_customer_id()} not found.")

            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product.get_product_id(),))
            if cursor.fetchone() is None:
                raise ProductNotFoundException(f"Product with ID {product.get_product_id()} not found.")

            query = "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)"
            cursor.execute(query, (
                customer.get_customer_id(),
                product.get_product_id(),
                quantity
            ))
            conn.commit()
            success = True
        except (CustomerNotFoundException, ProductNotFoundException) as e:
            print(e)
            raise
        except Exception as e:
            print(f"Error adding to cart: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def remove_from_cart(self, customer: Customer, product: Product) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer.get_customer_id(),))
            if cursor.fetchone() is None:
                raise CustomerNotFoundException(f"Customer with ID {customer.get_customer_id()} not found.")

            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product.get_product_id(),))
            if cursor.fetchone() is None:
                raise ProductNotFoundException(f"Product with ID {product.get_product_id()} not found.")

            query = "DELETE FROM cart WHERE customer_id = %s AND product_id = %s"
            cursor.execute(query, (
                customer.get_customer_id(),
                product.get_product_id()
            ))
            conn.commit()
            success = cursor.rowcount > 0
        except (CustomerNotFoundException, ProductNotFoundException) as e:
            print(e)
            raise
        except Exception as e:
            print(f"Error removing from cart: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def place_order(self, customer, cart_items: list, shipping_address: str) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            customer_id = customer.get_customer_id() if isinstance(customer, Customer) else customer

            conn = DBConnection.get_connection()
            cursor = conn.cursor()

            total_price = sum(item["product"].get_price() * item["quantity"] for item in cart_items)

            order_query = "INSERT INTO orders (customer_id, order_date, total_price, shipping_address) VALUES (%s, NOW(), %s, %s)"
            cursor.execute(order_query, (customer_id, total_price, shipping_address))
            order_id = cursor.lastrowid

            for item in cart_items:
                product_id = item["product"].get_product_id()
                quantity = item["quantity"]
                order_item_query = "INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)"
                cursor.execute(order_item_query, (order_id, product_id, quantity))

            conn.commit()
            success = True
        except Exception as e:
            print(f"Error placing order: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def get_orders_by_customer(self, customer_id: int):
        conn = None
        cursor = None
        orders = []
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if cursor.fetchone() is None:
                raise CustomerNotFoundException(f"Customer with ID {customer_id} not found.")

            query = "SELECT order_id, order_date, total_price, shipping_address FROM orders WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            orders = cursor.fetchall()

            if not orders:
                raise OrderNotFoundException(f"No orders found for Customer ID {customer_id}.")

        except (CustomerNotFoundException, OrderNotFoundException) as e:
            print(e)
            raise
        except Exception as e:
            print(f"Error retrieving orders: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return orders

    def get_all_from_cart(self, customer_id: int) -> list:
        conn = None
        cursor = None
        cart_items = []
        try:
            if isinstance(customer_id, Customer):
                customer_id = customer_id.get_customer_id()

            conn = DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT p.product_id, p.name, p.price, c.quantity
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.customer_id = %s
            """
            cursor.execute(query, (customer_id,))
            cart_items = cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving cart items: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return cart_items
