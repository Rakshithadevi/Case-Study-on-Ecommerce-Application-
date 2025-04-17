from dao.OrderProcessorRepository import OrderProcessorRepository
from entity.Customer import Customer
from entity.Product import Product
from entity.Admin import Admin
from entity.Order import Order
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

            # Check if customer exists
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer.get_customer_id(),))
            if cursor.fetchone() is None:
                raise CustomerNotFoundException(f"Customer with ID {customer.get_customer_id()} not found.")

            # Check if product exists
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product.get_product_id(),))
            if cursor.fetchone() is None:
                raise ProductNotFoundException(f"Product with ID {product.get_product_id()} not found.")

            # Insert into cart
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


            cursor.execute("""
                SELECT order_id, order_date, total_price, shipping_address
                FROM orders
                WHERE customer_id = %s
                ORDER BY order_date DESC
            """, (customer_id,))
            orders_data = cursor.fetchall()

            if not orders_data:
                raise OrderNotFoundException(f"No orders found for Customer ID {customer_id}.")


            for order in orders_data:
                order_id, order_date, total_price, shipping_address = order


                cursor.execute("""
                    SELECT p.name, p.price, oi.quantity
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.product_id
                    WHERE oi.order_id = %s
                """, (order_id,))
                items = cursor.fetchall()

                orders.append({
                    "order_id": order_id,
                    "order_date": order_date,
                    "total_price": total_price,
                    "shipping_address": shipping_address,
                    "items": [{"name": item[0], "price": item[1], "quantity": item[2]} for item in items]

                })

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

    def create_admin(self, admin) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO admin (name, password) VALUES (%s, %s)"
            cursor.execute(query, (
                admin.get_name(),
                admin.get_password()
            ))
            admin.set_admin_id(cursor.lastrowid)
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error creating admin: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success

    def view_all_customers(self) -> list[Customer]:
        conn = None
        cursor = None
        customers = []
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM customers"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                customer = Customer(row['customer_id'], row['name'], row['email'], row['password'])
                customers.append(customer)
        except Exception as e:
            print(f"Error fetching customers: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return customers

    def view_all_products(self):
        conn = None
        cursor = None
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()

            query = """
                SELECT 
                    p.product_id,
                    p.name,
                    p.price,
                    p.stockQuantity - IFNULL(SUM(c.quantity), 0) AS available_stock
                FROM 
                    products p
                LEFT JOIN 
                    cart c ON p.product_id = c.product_id
                GROUP BY 
                    p.product_id, p.name, p.price, p.stockQuantity
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("Error retrieving products:", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def view_customer_orders(self, customer_id: int) -> list[Order]:
        conn = None
        cursor = None
        orders = []
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if cursor.fetchone() is None:
                raise CustomerNotFoundException(f"Customer with ID {customer_id} not found.")

            query = "SELECT * FROM orders WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            rows = cursor.fetchall()

            if not rows:
                raise OrderNotFoundException(f"No orders found for customer ID {customer_id}.")

            for row in rows:
                order = Order(
                    order_id=row["order_id"],
                    customer_id=row["customer_id"],
                    order_date=row["order_date"],
                    total_price=row["total_price"],
                    shipping_address=row["shipping_address"]
                )
                orders.append(order)
        except (CustomerNotFoundException, OrderNotFoundException) as e:
            print(e)
            raise
        except Exception as e:
            print(f"Error viewing customer orders: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return orders

    def get_customer_by_email(self, email: str) -> Customer:
        conn = None
        cursor = None
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM customers WHERE email = %s"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row:
                return Customer(row['customer_id'], row['name'], row['email'], row['password'])
            else:
                raise CustomerNotFoundException(f"No customer found with email: {email}")
        except CustomerNotFoundException as e:
            # Just raise it; let the upper layer handle printing
            raise e
        except Exception as e:
            print(f"Error fetching customer by email: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def cancel_order(self, order_id: int) -> bool:
        conn = None
        cursor = None
        success = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM orders WHERE order_id = %s"
            cursor.execute(query, (order_id,))
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error canceling order: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return success
    def login_admin(self, name: str, password: str) -> bool:
        conn = None
        cursor = None
        is_authenticated = False
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM admin WHERE name = %s AND password = %s"
            cursor.execute(query, (name, password))
            if cursor.fetchone():
                is_authenticated = True
        except Exception as e:
            print(f"Error during admin login: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return is_authenticated

    def get_product_by_id(self, product_id: int):
        conn = None
        cursor = None
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor()

            query = "SELECT product_id, name, price, description, stockQuantity FROM products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()

            if row:
                return Product(
                    product_id=row[0],
                    name=row[1],
                    price=row[2],
                    description=row[3],
                    stock_quantity=row[4]
                )
            else:
                return None
        except Exception as e:
            print(f"Error fetching product by ID: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()






