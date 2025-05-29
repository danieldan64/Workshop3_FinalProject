import os
import json

# Constants
DATA_FILE = 'data/inventory.txt'
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"},
}

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Item Class
class Item:
    def __init__(self, item_id, name, quantity, price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def to_dict(self):
        return {
            "id": self.item_id,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
        }

    @staticmethod
    def from_dict(data):
        return Item(data["id"], data["name"], data["quantity"], data["price"])

# Inventory Class
class Inventory:
    def __init__(self):
        self.items = {}
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    for item in data:
                        self.items[item["id"]] = Item.from_dict(item)
        except Exception as e:
            print("Error loading inventory data:", e)

    def save_data(self):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump([item.to_dict() for item in self.items.values()], f, indent=2)
        except Exception as e:
            print("Error saving inventory data:", e)

    def add_item(self, item):
        if item.item_id in self.items:
            print("Item ID already exists.")
            return
        self.items[item.item_id] = item
        self.save_data()
        print("Item added successfully.")

    def update_item(self, item_id, name=None, quantity=None, price=None):
        item = self.items.get(item_id)
        if not item:
            print("Item not found.")
            return
        if name: item.name = name
        if quantity is not None: item.quantity = quantity
        if price is not None: item.price = price
        self.save_data()
        print("Item updated successfully.")

    def delete_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
            self.save_data()
            print("Item deleted successfully.")
        else:
            print("Item not found.")

    def view_items(self):
        if not self.items:
            print("No items in inventory.")
        for item in self.items.values():
            self.print_item(item)

    def search_item(self, keyword):
        found = False
        for item in self.items.values():
            if keyword.lower() in item.item_id.lower() or keyword.lower() in item.name.lower():
                self.print_item(item)
                found = True
        if not found:
            print("No matching item found.")

    def update_quantity(self, item_id, delta):
        item = self.items.get(item_id)
        if item:
            item.quantity += delta
            self.save_data()
            print("Stock updated successfully.")
        else:
            print("Item not found.")

    def generate_report(self):
        print("\n--- Low Stock Items ---")
        for item in self.items.values():
            if item.quantity <= 5:
                self.print_item(item)

        print("\n--- Total Inventory Value ---")
        total_value = sum(item.quantity * item.price for item in self.items.values())
        print(f"Total Value: ${total_value:.2f}")

    @staticmethod
    def print_item(item):
        print(f"ID: {item.item_id}, Name: {item.name}, Quantity: {item.quantity}, Price: ${item.price:.2f}")

# Basic login system
def login():
    print("--- Login ---")
    username = input("Username: ")
    password = input("Password: ")
    user = USERS.get(username)
    if user and user["password"] == password:
        return user["role"]
    else:
        print("Invalid credentials.")
        return None

# Input helpers
def get_non_empty(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        print("Input cannot be empty.")

def get_positive_number(prompt, type_=int):
    while True:
        try:
            value = type_(input(prompt))
            if value > 0:
                return value
            print("Enter a positive number.")
        except:
            print("Invalid input. Try again.")

# Main loop
def main():
    inv = Inventory()
    role = login()
    if not role:
        return

    while True:
        print("\n--- Inventory Menu ---")
        if role == "admin":
            print("1. Add Item\n2. View Items\n3. Search Item\n4. Update Item\n5. Delete Item\n6. Stock In/Out\n7. Generate Report\n0. Exit")
        else:
            print("1. View Items\n2. Search Item\n3. Stock In/Out\n0. Exit")

        choice = input("Choose an option: ")

        if role == "admin":
            if choice == '1':
                item_id = get_non_empty("Item ID: ")
                name = get_non_empty("Name: ")
                quantity = get_positive_number("Quantity: ")
                price = get_positive_number("Price: ", float)
                inv.add_item(Item(item_id, name, quantity, price))
            elif choice == '2':
                inv.view_items()
            elif choice == '3':
                keyword = get_non_empty("Enter ID or Name to search: ")
                inv.search_item(keyword)
            elif choice == '4':
                item_id = get_non_empty("Item ID to update: ")
                name = input("New name (leave blank to keep): ")
                quantity = input("New quantity (leave blank to keep): ")
                price = input("New price (leave blank to keep): ")
                inv.update_item(
                    item_id,
                    name=name if name.strip() else None,
                    quantity=int(quantity) if quantity.strip().isdigit() else None,
                    price=float(price) if price.strip().replace('.', '', 1).isdigit() else None
                )
            elif choice == '5':
                item_id = get_non_empty("Item ID to delete: ")
                inv.delete_item(item_id)
            elif choice == '6':
                item_id = get_non_empty("Item ID: ")
                delta = int(input("Enter quantity to add/subtract: "))
                inv.update_quantity(item_id, delta)
            elif choice == '7':
                inv.generate_report()
            elif choice == '0':
                break

        else:
            if choice == '1':
                inv.view_items()
            elif choice == '2':
                keyword = get_non_empty("Enter ID or Name to search: ")
                inv.search_item(keyword)
            elif choice == '3':
                item_id = get_non_empty("Item ID: ")
                delta = int(input("Enter quantity to add/subtract: "))
                inv.update_quantity(item_id, delta)
            elif choice == '0':
                break

if __name__ == "__main__":
    main()
