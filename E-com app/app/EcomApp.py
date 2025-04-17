import sys
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from entity.Customer import Customer
from entity.Product import Product
from entity.Admin import Admin
from exception.customer_not_found_exception import CustomerNotFoundException
from exception.product_not_found_exception import ProductNotFoundException
from exception.order_not_found_exception import OrderNotFoundException

class EcomApp:
    def __init__(self):
        self.order_repo = OrderProcessorRepositoryImpl()
        self.logged_in_user = None
        self.is_admin = False
    def login(self):
        print("===== Welcome to E-commerce App =====")
        print("1. Sign In")
        print("2. Sign Up")
        choice = input("Enter your choice (1 or 2): ")
        if choice == "1":
            self.sign_in()
        elif choice == "2":
            self.sign_up()
        else:
            print("Invalid input. Try again.")
            self.login()
    def sign_in(self):
        print("\n===== Sign In =====")
        user_type = input("Are you a (1) Admin or (2) Customer? Enter 1 or 2: ")
        if user_type == "1":
            self.admin_login()
        elif user_type == "2":
            self.customer_login()
        else:
            print("Invalid choice! Please select 1 for Admin or 2 for Customer.")
            self.sign_in()
    def sign_up(self):
        print("\n===== Sign Up =====")
        user_type = input("Sign up as (1) Admin or (2) Customer? Enter 1 or 2: ")

        if user_type == "1":
            name = input("Enter admin name: ")
            password = input("Enter admin password: ")
            self.create_admin(name, password)
        elif user_type == "2":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            customer = Customer(name=name, email=email, password=password)
            if self.order_repo.create_customer(customer):
                print("Customer account created successfully! You can now log in.")
            else:
                print("Failed to create customer account.")
            self.login()
        else:
            print("Invalid choice! Please select 1 for Admin or 2 for Customer.")
            self.sign_up()

    def create_admin(self, name, password):
        admin = Admin(name=name, password=password)
        if self.order_repo.create_admin(admin):
            print("Admin account created successfully!")
        else:
            print("Failed to create admin account.")
        self.login()
    def create_customer(self, name, email, password):
        customer = Customer(name=name, email=email, password=password)
        return self.order_repo.create_customer(customer)
    def admin_login(self):
        admin_name = input("Enter admin name: ").strip()
        admin_password = input("Enter admin password: ").strip()

        if self.order_repo.login_admin(admin_name, admin_password):
            self.is_admin = True
            print("Admin login successful!")
            self.admin_menu()
        else:
            print("Invalid admin credentials! Please try again.")
            self.login()

    def customer_login(self):
        print("\n===== Customer Sign In =====")
        email = input("Enter customer email: ")
        password = input("Enter customer password: ")
        try:
            customer = self.order_repo.get_customer_by_email(email)
            if customer and customer.get_password() == password:
                self.logged_in_user = customer
                print("Customer login successful!")
                self.customer_menu(customer)
            else:
                print("Incorrect password. Please try again.")
        except CustomerNotFoundException as e:
            print(str(e))

    def admin_menu(self):
        while True:
            print("\n===== Admin Dashboard =====")
            print("1. View Customers")
            print("2. View Products")
            print("3. View Customer Orders")
            print("4. Add Product")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_customers()
            elif choice == "2":
                self.view_products()
            elif choice == "3":
                self.view_customer_orders()
            elif choice == "4":
                self.create_product()
            elif choice == "5":
                print("Logging out...")
                self.logged_in_user = None
                self.is_admin = False
                self.login()
            else:
                print("Invalid choice! Please enter a number from 1 to 5.")

    def customer_menu(self,customer):
        while True:
            print("\n===== Customer Dashboard =====")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. View Cart")
            print("5. Place Order")
            print("6. View Customer Orders")
            print("7. Cancel Order")
            print("8. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_products()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.remove_from_cart()
            elif choice == "4":
                self.view_cart()
            elif choice == "5":
                self.place_order()
            elif choice == "6":
                self.view_orders()
            elif choice == "7":
                self.cancel_order()
            elif choice == "8":
                print("Logging out...")
                self.logged_in_user = None
                self.is_admin = False
                self.login()
            else:
                print("Invalid choice! Please enter a number from 1 to 8.")

    def view_customers(self):

        customers = self.order_repo.view_all_customers()
        if customers:
            print("Customers:")
            for customer in customers:
                print(f"ID: {customer.get_customer_id()}, Name: {customer.get_name()}, Email: {customer.get_email()}")
        else:
            print("No customers found.")

    def view_products(self):
        try:
            products = self.order_repo.view_all_products()
            if products:
                print("Products:")
                for product in products:
                    print(
                        f"ID: {product[0]}, Name: {product[1]}, Price: ₹{product[2]:.2f}, Stock Available: {product[3]}")
            else:
                print("No products found.")
        except Exception as e:
            print("Error retrieving products:", e)

    def view_customer_orders(self):
        try:
            customer_id = int(input("Enter customer ID to view orders: "))
            orders = self.order_repo.get_orders_by_customer(customer_id)

            if orders:
                print("Orders:")
                for order in orders:
                    print(
                        f"Order ID: {order['order_id']}, Date: {order['order_date']}, Total Price: {order['total_price']}, Shipping Address: {order['shipping_address']}")
                    print("Items:")
                    for item in order["items"]:
                        print(f" - {item['name']} (x{item['quantity']}): {item['price']} each")
            else:
                print("No orders found.")
        except Exception as e:
            print("An error occurred while viewing orders:", e)


    def create_product(self):
        name = input("Enter product name: ")
        price = float(input("Enter product price: "))
        description = input("Enter product description: ")
        stock_quantity = int(input("Enter stock quantity: "))
        product = Product(name=name, price=price, description=description, stock_quantity=stock_quantity)
        if self.order_repo.create_product(product):
            print("Product created successfully!")
        else:
            print("Failed to create product.")

    def add_to_cart(self):
        try:
            if self.logged_in_user is None:
                print("Please login first.")
                return

            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity: "))
            customer_id = self.logged_in_user.get_customer_id()

            product = self.order_repo.get_product_by_id(product_id)
            if product is None:
                raise ProductNotFoundException("Product not found.")

            success = self.order_repo.add_to_cart(self.logged_in_user, product, quantity)
            if success:
                print("Product added to cart successfully!")
            else:
                print("Failed to add product to cart.")
        except ProductNotFoundException as e:
            print(f"Error: {e}")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def remove_from_cart(self):
        try:
            if self.logged_in_user is None:
                print("Please login first.")
                return

            product_id = int(input("Enter product ID to remove: "))
            customer_id = self.logged_in_user.get_customer_id()

            product = self.order_repo.get_product_by_id(product_id)
            if product is None:
                raise ProductNotFoundException("Product not found.")

            if self.order_repo.remove_from_cart(self.logged_in_user, product):
                print("Product removed from cart successfully!")
            else:
                print("Product not found in cart.")
        except ProductNotFoundException as e:
            print(f"Error: {e}")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def view_cart(self):
        try:
            if self.logged_in_user is None:
                print("Please login first.")
                return

            customer_id = self.logged_in_user.get_customer_id()
            cart_items = self.order_repo.get_all_from_cart(customer_id)

            if cart_items:
                print("Cart Items:")
                for item in cart_items:
                    print(
                        f"Product ID: {item['product_id']}, Name: {item['name']}, Price: ₹{item['price']}, Quantity: {item['quantity']}")
            else:
                print("Cart is empty.")
        except CustomerNotFoundException:
            print("Error: Customer not found.")
        except Exception as e:
            print("Unexpected error:", e)

    def place_order(self):
        try:
            if self.logged_in_user is None:
                print("Please login first.")
                return

            customer_id = self.logged_in_user.get_customer_id()
            shipping_address = input("Enter shipping address: ")
            cart_items = self.order_repo.get_all_from_cart(customer_id)

            if cart_items:
                order_items = [
                    {"product": Product(
                        product_id=item["product_id"],
                        name=item["name"],
                        price=item["price"],
                        description="",
                        stock_quantity=0
                    ), "quantity": item["quantity"]}
                    for item in cart_items
                ]

                if self.order_repo.place_order(customer_id, order_items, shipping_address):
                    print("Order placed successfully!")
                else:
                    print("Failed to place order.")
            else:
                print("Cart is empty.")
        except OrderNotFoundException:
            print("Error: Unable to place order.")
        except Exception as e:
            print("Unexpected error:", e)

    def view_orders(self):
        try:
            if self.logged_in_user is None:
                print("Please login first.")
                return

            customer_id = self.logged_in_user.get_customer_id()
            orders = self.order_repo.get_orders_by_customer(customer_id)

            if orders:
                for order in orders:
                    print(f"Order ID: {order['order_id']}, Shipping Address: {order['shipping_address']}, Total Amount: ₹{order['total_price']}")
            else:
                print("No orders found.")
        except CustomerNotFoundException:
            print("Error: Customer not found.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def cancel_order(self):
        try:
            if self.logged_in_user is None:
                print("Please login first.")
                return

            order_id = int(input("Enter order ID to cancel: "))
            if self.order_repo.cancel_order(order_id):
                print("Order canceled successfully.")
            else:
                print("Failed to cancel order.")
        except OrderNotFoundException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    app = EcomApp()
    app.login()
