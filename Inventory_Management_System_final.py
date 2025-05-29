import os
import sys
from pathlib import Path

# Constants
DOCUMENTS_DIR = Path.home() / "Documents"
INVENTORY_FILE = DOCUMENTS_DIR / "inventory.txt"
MIN_STOCK_ALERT = 10


def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize_inventory_file():
    """Create inventory file if it doesn't exist"""
    try:
        DOCUMENTS_DIR.mkdir(exist_ok=True)
        if not INVENTORY_FILE.exists():
            INVENTORY_FILE.touch()
    except Exception as e:
        print(f"❌ Error creating inventory file: {e}")
        sys.exit(1)


def load_inventory():
    """Load inventory from file"""
    inventory = []
    try:
        with open(INVENTORY_FILE, 'r') as file:
            for line in file:
                if line.strip():
                    item_id, name, quantity, price = line.strip().split(',')
                    inventory.append({
                        'id': int(item_id),
                        'name': name,
                        'quantity': int(quantity),
                        'price': float(price)
                    })
    except FileNotFoundError:
        initialize_inventory_file()
        return []
    except Exception as e:
        print(f"❌ Error reading inventory: {e}")
        return []
    return inventory


def save_inventory(inventory):
    """Save inventory to file"""
    try:
        with open(INVENTORY_FILE, 'w') as file:
            for item in inventory:
                file.write(f"{item['id']},{item['name']},{item['quantity']},{item['price']}\n")
    except Exception as e:
        print(f"❌ Error saving inventory: {e}")


def generate_new_id(inventory):
    """Generate a new unique ID"""
    if not inventory:
        return 1
    max_id = max(item['id'] for item in inventory)
    return max_id + 1


def display_main_menu():
    """Display the main menu"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║    INVENTORY MANAGEMENT SYSTEM   ║")
    print("╠══════════════════════════════════╣")
    print("║ 1. Add New Item                  ║")
    print("║ 2. View All Items                ║")
    print("║ 3. Search Item                   ║")
    print("║ 4. Update Item                   ║")
    print("║ 5. Delete Item                   ║")
    print("║ 6. Adjust Stock (+/-)            ║")
    print("║ 7. Generate Reports              ║")
    print("║ 8. Exit                          ║")
    print("╚══════════════════════════════════╝")


def get_valid_input(prompt, input_type=str, allow_back=True):
    """Get validated user input with option to go back"""
    while True:
        user_input = input(prompt).strip()

        if allow_back and user_input.lower() in ('b', 'back'):
            return None

        try:
            if input_type == str:
                if not user_input:
                    raise ValueError("Input cannot be empty")
                return user_input
            elif input_type == int:
                value = int(user_input)
                if value < 0:
                    raise ValueError("Value must be positive")
                return value
            elif input_type == float:
                value = float(user_input)
                if value < 0:
                    raise ValueError("Value must be positive")
                return value
        except ValueError as e:
            print(f"❌ Invalid input: {e}. Please try again.")


def add_item(inventory):
    """Add a new item to inventory"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║         ADD NEW ITEM             ║")
    print("╚══════════════════════════════════╝")

    name = get_valid_input("Enter Item Name (or 'B' to go back): ", str)
    if name is None:
        return

    quantity = get_valid_input("Enter Quantity: ", int)
    if quantity is None:
        return

    price = get_valid_input("Enter Price ($): ", float)
    if price is None:
        return

    new_id = generate_new_id(inventory)

    # Check if ID exists (shouldn't happen with auto-increment, but just in case)
    while any(item['id'] == new_id for item in inventory):
        new_id += 1

    inventory.append({
        'id': new_id,
        'name': name,
        'quantity': quantity,
        'price': price
    })

    save_inventory(inventory)
    print(f"\n✅ Success! Item '{name}' (ID: {new_id}) added.")
    input("\nPress Enter to continue...")


def view_all_items(inventory):
    """Display all items in inventory"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║         CURRENT INVENTORY        ║")
    print("╠══════════════════════════════════╣")

    if not inventory:
        print("║        No items in inventory       ║")
    else:
        print("║ ID   Name                 Qty  Price ║")
        print("╠══════════════════════════════════╣")
        for item in inventory:
            print(f"║ {item['id']:<4} {item['name'][:18]:<18} {item['quantity']:>4}  ${item['price']:>6.2f} ║")

    print("╚══════════════════════════════════╝")
    input("\nPress Enter to return to menu...")


def search_item(inventory):
    """Search for items by ID or name"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║           SEARCH ITEM            ║")
    print("╚══════════════════════════════════╝")

    search_term = get_valid_input("Enter ID or Name to search (or 'B' to go back): ", str)
    if search_term is None:
        return

    results = []
    try:
        # Try searching by ID first
        search_id = int(search_term)
        results = [item for item in inventory if item['id'] == search_id]
    except ValueError:
        # Search by name if ID conversion fails
        results = [item for item in inventory if search_term.lower() in item['name'].lower()]

    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║         SEARCH RESULTS           ║")
    print("╠══════════════════════════════════╣")

    if not results:
        print("║        No matching items found     ║")
    else:
        print("║ ID   Name                 Qty  Price ║")
        print("╠══════════════════════════════════╣")
        for item in results:
            print(f"║ {item['id']:<4} {item['name'][:18]:<18} {item['quantity']:>4}  ${item['price']:>6.2f} ║")

    print("╚══════════════════════════════════╝")
    input("\nPress Enter to return to menu...")


def update_item(inventory):
    """Update item details"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║          UPDATE ITEM             ║")
    print("╚══════════════════════════════════╝")

    item_id = get_valid_input("Enter Item ID to update (or 'B' to go back): ", int)
    if item_id is None:
        return

    item = next((i for i in inventory if i['id'] == item_id), None)
    if not item:
        print(f"❌ Item with ID {item_id} not found.")
        input("\nPress Enter to continue...")
        return

    print(f"\nCurrent Details:")
    print(f"1. Name: {item['name']}")
    print(f"2. Quantity: {item['quantity']}")
    print(f"3. Price: ${item['price']:.2f}")

    field = get_valid_input("\nEnter number of field to update (1-3) or 'B' to go back: ", int)
    if field is None:
        return

    if field == 1:
        new_name = get_valid_input(f"Enter new name (current: {item['name']}): ", str)
        if new_name is not None:
            item['name'] = new_name
    elif field == 2:
        new_quantity = get_valid_input(f"Enter new quantity (current: {item['quantity']}): ", int)
        if new_quantity is not None:
            item['quantity'] = new_quantity
    elif field == 3:
        new_price = get_valid_input(f"Enter new price (current: ${item['price']:.2f}): $", float)
        if new_price is not None:
            item['price'] = new_price
    else:
        print("❌ Invalid field selection.")
        input("\nPress Enter to continue...")
        return

    save_inventory(inventory)
    print("\n✅ Item updated successfully!")
    input("\nPress Enter to continue...")


def delete_item(inventory):
    """Delete an item from inventory"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║          DELETE ITEM             ║")
    print("╚══════════════════════════════════╝")

    item_id = get_valid_input("Enter Item ID to delete (or 'B' to go back): ", int)
    if item_id is None:
        return

    item = next((i for i in inventory if i['id'] == item_id), None)
    if not item:
        print(f"❌ Item with ID {item_id} not found.")
        input("\nPress Enter to continue...")
        return

    confirm = input(f"Are you sure you want to delete '{item['name']}' (ID: {item_id})? (Y/N): ").strip().lower()
    if confirm == 'y':
        inventory[:] = [i for i in inventory if i['id'] != item_id]
        save_inventory(inventory)
        print("\n✅ Item deleted successfully!")
    else:
        print("\nDeletion cancelled.")

    input("\nPress Enter to continue...")


def adjust_stock(inventory):
    """Add or remove stock quantity"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║         ADJUST STOCK             ║")
    print("╚══════════════════════════════════╝")

    item_id = get_valid_input("Enter Item ID to adjust (or 'B' to go back): ", int)
    if item_id is None:
        return

    item = next((i for i in inventory if i['id'] == item_id), None)
    if not item:
        print(f"❌ Item with ID {item_id} not found.")
        input("\nPress Enter to continue...")
        return

    print(f"\nCurrent stock for '{item['name']}': {item['quantity']}")
    adjustment = get_valid_input("Enter adjustment (+/- quantity, e.g., +5 or -3): ", str)
    if adjustment is None:
        return

    try:
        # Check if input starts with + or -
        if adjustment.startswith(('+', '-')):
            change = int(adjustment)
            new_quantity = item['quantity'] + change
            if new_quantity < 0:
                print("❌ Error: Resulting quantity cannot be negative.")
                input("\nPress Enter to continue...")
                return

            item['quantity'] = new_quantity
            save_inventory(inventory)
            print(f"\n✅ Stock updated. New quantity: {new_quantity}")
        else:
            print("❌ Invalid input. Please use + or - before the number.")
    except ValueError:
        print("❌ Invalid input. Please enter a valid number after + or -.")

    input("\nPress Enter to continue...")


def generate_reports(inventory):
    """Generate inventory reports"""
    clear_screen()
    print("╔══════════════════════════════════╗")
    print("║          INVENTORY REPORTS       ║")
    print("╠══════════════════════════════════╣")
    print("║ 1. Low Stock Alert               ║")
    print("║ 2. Total Inventory Value         ║")
    print("║ 3. Back to Main Menu             ║")
    print("╚══════════════════════════════════╝")

    choice = get_valid_input("\nSelect report option (1-3): ", int, allow_back=False)

    if choice == 1:
        # Low stock report
        low_stock = [item for item in inventory if item['quantity'] < MIN_STOCK_ALERT]

        clear_screen()
        print("╔══════════════════════════════════╗")
        print("║         LOW STOCK ALERT          ║")
        print("╠══════════════════════════════════╣")

        if not low_stock:
            print("║    No items below stock threshold   ║")
        else:
            print(f"⚠ Items below {MIN_STOCK_ALERT} units:")
            print("║ ID   Name                 Qty  Price ║")
            print("╠══════════════════════════════════╣")
            for item in low_stock:
                print(f"║ {item['id']:<4} {item['name'][:18]:<18} {item['quantity']:>4}  ${item['price']:>6.2f} ║")

        print("╚══════════════════════════════════╝")
        input("\nPress Enter to continue...")

    elif choice == 2:
        # Total inventory value
        total_value = sum(item['quantity'] * item['price'] for item in inventory)

        clear_screen()
        print("╔══════════════════════════════════╗")
        print("║     TOTAL INVENTORY VALUE        ║")
        print("╠══════════════════════════════════╣")
        print(f"║ Total Value: ${total_value:>12,.2f} ║")
        print("╚══════════════════════════════════╝")
        input("\nPress Enter to continue...")

    elif choice == 3:
        return


def main():
    """Main program loop"""
    initialize_inventory_file()
    inventory = load_inventory()

    while True:
        display_main_menu()
        choice = get_valid_input("\nSelect an option (1-8): ", int, allow_back=False)

        if choice == 1:
            add_item(inventory)
        elif choice == 2:
            view_all_items(inventory)
        elif choice == 3:
            search_item(inventory)
        elif choice == 4:
            update_item(inventory)
        elif choice == 5:
            delete_item(inventory)
        elif choice == 6:
            adjust_stock(inventory)
        elif choice == 7:
            generate_reports(inventory)
        elif choice == 8:
            print("\nThank you for using the Inventory Management System!")
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid option. Please select 1-8.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()1