import datetime

# Defining function by class
class Product:
    def __init__(self, product_number, name, price, stock):
        self.product_number = product_number
        self.name = name
        self.price = price
        self.stock = stock

# function how item is added to shopping cart
class ShoppingCart:
    def __init__(self):
        self.items = {}
    def add_item(self, product, quantity):
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return
        if product.stock >= quantity:
            if product.product_number in self.items:
                self.items[product.product_number] += quantity
            else:
                self.items[product.product_number] = quantity
            product.stock -= quantity
            print(f"Added {quantity} {product.name}(s) to the cart.")
        else:
            print(f"Insufficient stock! Only {product.stock} item(s) available.")

# function that determine how items is remove from shopping cart
    def remove_item(self, product_number, quantity, products):
        if product_number in self.items:
            if quantity <= self.items[product_number]:
                self.items[product_number] -= quantity
                product = products[product_number]
                product.stock += quantity
                if self.items[product_number] == 0:
                    del self.items[product_number]
                print(f"Removed {quantity} {product_number}(s) from the cart.")
            else:
                print("trying to remove more items than are in the cart.")
        else:
            print("Products not in cart.")

# define how to view cart when items is added to the cart
    def view_cart(self, products):
        print("\n Shopping Cart ")
        if not self.items:
            print("cart is empty.")
            return
        subtotal = 0
        for product_number, quantity in self.items.items():
            product = products[product_number]
            total = product.price * quantity
            subtotal += total
            print(f"{product.name}: {quantity} x ${product.price:.2f} = ${total:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")

# Function that calculate price and discount.
    def calculate_totals(self, products):
        subtotal = 0
        for product_number, quantity in self.items.items():
            product = products[product_number]
            subtotal += product.price * quantity
        discount = 0.05 * subtotal if subtotal > 5000 else 0
        taxed_amount = (subtotal - discount) * 0.10
        total = subtotal - discount + taxed_amount
        return subtotal, discount, taxed_amount, total

    def clear_cart(self):
        self.items.clear()


class POS_System:
    def __init__(self):
        self.products = {}
        self.cart = ShoppingCart()
        self.receipt_number = 1

# List containing product list
    def load_products(self):
        product_data = {
            1: ("Flour", 145.50, 20),
            2: ("Rice", 135.00, 30),
            3: ("Sugar", 156.00, 25),
            4: ("Cornmeal", 200.00, 15),
            5: ("Oats", 120.50, 10),
            6: ("Milk", 300.00, 8),
            7: ("Water Cracker", 275.00, 5),
            8: ("Bake Bean", 350.50, 12),
            9: ("National Bun", 450.00, 6),
            10: ("Jif Peanut Butter", 700.75, 7)
        }
        for product_number, (name, price, stock) in product_data.items():
            self.products[product_number] = Product(product_number, name, price, stock)

# display function of the cart
    def display_catalog(self):
        print("\n Products Catalog ")
        for product in self.products.values():
            print(
                f"Product ID: ${product.product_number} | {product.name}: ${product.price:.2f} | stock: {product.stock}")
            if product.stock < 5:
                print(f"** Low Stock Alert: Only {product.stock} left! **")

# allowing the system to check out items place in the cart adding tax, discount, and giving total also return function
    def checkout(self):
        if not self.cart.items:
            print("Cart is empty! Add items before checkout.")
            return

        while True:
            subtotal, discount, tax, total = self.cart.calculate_totals(self.products)
            print(f"\nSubtotal: ${subtotal:.2f}")
            print(f"Discount: ${discount:.2f}")
            print(f"Sales Tax (10%): ${tax:.2f}")
            print(f"Total Due: ${total:.2f}")

            choice = input(
                "\nDo you want to (1) Proceed to Payment, (2) Add item, (3) Remove item, (4) Cancel checkout: ").strip()

            if choice == '1':
                while True:
                    try:
                        received = float(input("Enter amount received: $"))
                        if received < total:
                            print("Insufficient payment! Try again.")
                        else:
                            change = received - total
                            self.generate_receipt(subtotal, discount, tax, total, received, change)
                            self.receipt_number += 1
                            self.cart.clear_cart()
                            break
                    except ValueError:
                        print("Invalid input! Please enter a valid number.")
                break
            elif choice == '2':
                product_number = input("Enter product ID: ").strip()
                try:
                    product_number = int(product_number)
                    if product_number not in self.products:
                        print("Product not found!")
                        continue
                    quantity = int(input("Enter quantity: "))
                    self.cart.add_item(self.products[product_number], quantity)
                except ValueError:
                    print("Invalid input! Quantity must be a number.")
            elif choice == '3':
                product_number = input("Enter product ID to remove: ").strip()
                try:
                    product_number = int(product_number)
                    if product_number not in self.products:
                        print("product not found!")
                        continue
                    quantity = int(input("Enter quantity to remove: "))
                    self.cart.remove_item(product_number, quantity, self.products)
                except ValueError:
                    print("Invalid input! Quantity must be a number.")
            elif choice == '4':
                print("canceling checkout...")
                break
            elif choice == '5':
                self.cart.view_cart(self.products)
            else:
                print("Invalid choice. Please choose a valid option.")

# function displaying items, amount, and total on receipt
    def generate_receipt(self, subtotal, discount, tax, total, received, change):
        print("\n RECEIPT ")
        print(f" RECEIPT #{self.receipt_number}")
        print(" Best Buy Retail Store")
        print(" Date:", datetime.datetime.now().strftime("%Y-%m-%d"))
        print(" Time:", datetime.datetime.now().strftime("%I:%M %p"))
        print("")
        for product_number, quantity in self.cart.items.items():
            product = self.products[product_number]
            line_total = quantity * product.price
            print(f"{product.name}: {quantity} x ${product.price:.2f} = ${line_total:.2f}")
        print("")
        print(f"Subtotal       : ${subtotal:.2f}")
        print(f"Discount       : -${discount:.2f}")
        print(f"Sales Tax (10%): ${tax:.2f}")
        print(f"TOTAL          : ${total:.2f}")
        print(f"Amount Paid    : ${received:.2f}")
        print(f"Change         : ${change:.2f}")
        print("")
        print("Thank you for shopping with BB Wholesale!")
        print("\n")

# this function display the main menu allowing the user to select different options
    def run(self):
        self.load_products()
        while True:
            print("\n Welcome to Best Buy Wholesale ")
            print("1. View Product Catalog")
            print("2. Add Item to Cart")
            print("3. Remove Item from Cart")
            print("4. View Cart")
            print("5. Checkout")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ").strip()

            if choice == '1':
                self.display_catalog()
            elif choice == '2':
                product_number = input("Enter product ID: ").strip()
                try:
                    product_number = int(product_number)
                    if product_number not in self.products:
                        print("Product not found!")
                        continue
                    quantity = int(input("Enter quantity: "))
                    self.cart.add_item(self.products[product_number], quantity)
                except ValueError:
                    print("Invalid input! Quantity must be a number.")
            elif choice == '3':
                product_number = input("Enter product ID to remove: ").strip()
                try:
                    product_number = int(product_number)
                    print("product not found!")
                    continue
                    quantity = int(input("Enter quantity to remove: "))
                    self.cart.remove_item(name, quantity, self.products)
                except ValueError:
                    print("Invalid input! Quantity must be a number.")
            elif choice == '4':
                self.cart.view_cart(self.products)
            elif choice == '5':
                self.checkout()
            elif choice == '6':
                print("Thank you! Exiting system...")
                break
            else:
                print("Invalid choice. Please select between 1 and 6.")


if __name__ == "__main__":
    pos = POS_System()
    pos.run()