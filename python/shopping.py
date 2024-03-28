# This Code is Written by Nitin Swami 
class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class ShoppingCart:
    def __init__(self, items_available):
        self.items_available = items_available
        self.cart = []

    def display_menu(self):
        print("Available Items:")
        for item in self.items_available:
            print(f"{item.name} - Quantity: {item.quantity}, Price: ₹{item.price}")

    def add_to_cart(self, item_name, quantity):
        for item in self.items_available:
            if item.name == item_name:
                if item.quantity >= quantity:
                    self.cart.append((item, quantity))
                    item.quantity -= quantity
                    print(f"{quantity} {item.name}(s) added to cart.")
                else:
                    print(f"Sorry, only {item.quantity} {item.name}(s) available.")
                return
        print("Item not found.")

    def calculate_total(self):
        total = 0
        for item, quantity in self.cart:
            total += item.price * quantity
        return total

class Customer:
    def __init__(self, name, address, distance_from_store):
        self.name = name
        self.address = address
        self.distance_from_store = distance_from_store

def calculate_delivery_charges(distance_from_store):
    if distance_from_store <= 15:
        return 50
    elif distance_from_store <= 30:
        return 100
    else:
        return 0  # Free delivery beyond 30 km

def main():
    items_available = [
        Item("Biscuits", 30, 10),
        Item("Cereals", 20, 15),
        Item("Chicken", 15, 20)
    ]
    cart = ShoppingCart(items_available)
    customer_name = input("Enter your name: ")
    customer_address = input("Enter your address: ")
    distance_from_store = float(input("Enter distance from the store (in km): "))
    customer = Customer(customer_name, customer_address, distance_from_store)

    cart.display_menu()

    while True:
        item_name = input("Enter item name to add to cart (or 'done' to finish): ")
        if item_name.lower() == 'done':
            break
        quantity = int(input("Enter quantity: "))
        cart.add_to_cart(item_name, quantity)

    total_bill = cart.calculate_total()
    delivery_charges = calculate_delivery_charges(customer.distance_from_store)
    final_bill = total_bill + delivery_charges

    print("\n----- Final Bill -----")
    print("Customer Name:", customer.name)
    print("Customer Address:", customer.address)
    print("Total Bill: ₹", total_bill)
    print("Delivery Charges: ₹", delivery_charges)
    print("Final Bill: ₹", final_bill)

if __name__ == "__main__":
    main()
