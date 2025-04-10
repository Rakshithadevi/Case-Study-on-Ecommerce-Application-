import sys
from dao.OrderProcessorRepositoryImpl import OrderProcessorRepositoryImpl
from entity.Customer import Customer
from entity.Product import Product
from exception.customer_not_found_exception import CustomerNotFoundException
from exception.product_not_found_exception import ProductNotFoundException
from exception.order_not_found_exception import OrderNotFoundException


class EcomApp:
    def __init__(self):
        self.order_repo = OrderProcessorRepositoryImpl()

    def menu(self):
        while True:
            print("\n===== E-Commerce System =====")
            print("1. Register Customer")
            print("2. Create Product")
            print("3. Delete Product")
            print("4. Delete Customer")
            print("5. Add to Cart")
            print("6. Remove from Cart")
            print("7. View Cart")
            print("8. Place Order")
            print("9. View Customer Order")
            print("10. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_customer()
            elif choice == "2":
                self.create_product()
            elif choice == "3":
                self.delete_product()
            elif choice == "4":
                self.delete_customer()
            elif choice == "5":
                self.add_to_cart()
            elif choice == "6":
                self.remove_from_cart()
            elif choice == "7":
                self.view_cart()
            elif choice == "8":
                self.place_order()
            elif choice == "9":
                self.view_orders()
            elif choice == "10":
                print("Exiting... Goodbye!")
                sys.exit()
            else:
                print("Invalid choice! Please enter a number from 1 to 10.")

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

    def create_customer(self):
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        password = input("Enter password: ")
        customer = Customer(name=name, email=email, password=password)
        if self.order_repo.create_customer(customer):
            print("Customer created successfully!")
        else:
            print("Failed to create customer.")

    def delete_product(self):
        try:
            product_id = int(input("Enter product ID to delete: "))
            if self.order_repo.delete_product(product_id):
                print("Product deleted successfully!")
            else:
                print("Product not found.")
        except ProductNotFoundException:
            print("Error: Product not found.")

    def delete_customer(self):
        try:
            customer_id = int(input("Enter customer ID to delete: "))
            if self.order_repo.delete_customer(customer_id):
                print("Customer deleted successfully!")
            else:
                print("Customer not found.")
        except CustomerNotFoundException:
            print("Error: Customer not found.")

    def add_to_cart(self):
        try:
            customer_id = int(input("Enter customer ID: "))
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity: "))
            customer = Customer(customer_id=customer_id, name="", email="", password="")
            product = Product(product_id=product_id, name="", price=0, description="", stock_quantity=0)
            if self.order_repo.add_to_cart(customer, product, quantity):
                print("Product added to cart successfully!")
            else:
                print("Failed to add product to cart.")
        except ProductNotFoundException:
            print("Error: Product not found.")
        except CustomerNotFoundException:
            print("Error: Customer not found.")

    def remove_from_cart(self):
        try:
            customer_id = int(input("Enter customer ID: "))
            product_id = int(input("Enter product ID: "))
            customer = Customer(customer_id=customer_id, name="", email="", password="")
            product = Product(product_id=product_id, name="", price=0, description="", stock_quantity=0)
            if self.order_repo.remove_from_cart(customer, product):
                print("Product removed from cart successfully!")
            else:
                print("Product not found in cart.")
        except ProductNotFoundException:
            print("Error: Product not found.")
        except CustomerNotFoundException:
            print("Error: Customer not found.")

    def view_cart(self):
        try:
            customer_id = int(input("Enter customer ID: "))

            # ✅ Pass only the ID, not a Customer object
            cart_items = self.order_repo.get_all_from_cart(customer_id)

            if cart_items:
                print("Cart Items:")
                for item in cart_items:
                    print(
                        f"Product ID: {item['product_id']}, Name: {item['name']}, Price: {item['price']}, Quantity: {item['quantity']}")
            else:
                print("Cart is empty.")
        except CustomerNotFoundException:
            print("Error: Customer not found.")

    def place_order(self):
        try:
            customer_id = int(input("Enter customer ID: "))
            shipping_address = input("Enter shipping address: ")

            # ✅ Pass only the ID, not a Customer object
            cart_items = self.order_repo.get_all_from_cart(customer_id)

            if cart_items:
                order_items = [
                    {"product": Product(
                        product_id=item["product_id"],
                        name=item["name"],
                        price=item["price"],
                        description="",
                        stock_quantity=0
                    ),
                        "quantity": item["quantity"]}
                    for item in cart_items
                ]

                if self.order_repo.place_order(customer_id, order_items,
                                               shipping_address):  # ✅ Pass customer_id instead of object
                    print("Order placed successfully!")
                else:
                    print("Failed to place order.")
            else:
                print("Cart is empty.")
        except OrderNotFoundException:
            print("Error: Unable to place order.")

    def view_orders(self):
        try:
            customer_id = int(input("Enter customer ID: "))
            orders = self.order_repo.get_orders_by_customer(customer_id)
            if orders:
                print("Orders:")
                for order in orders:
                    print(
                        f"Order ID: {order[0]}, Date: {order[1]}, Total Price: {order[2]}, Shipping Address: {order[3]}")
            else:
                print("No orders found.")
        except CustomerNotFoundException:
            print("Error: Customer not found.")


if __name__ == "__main__":
    app = EcomApp()
    app.menu()
