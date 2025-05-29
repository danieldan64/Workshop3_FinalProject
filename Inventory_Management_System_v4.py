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
                file.write(f"{item['id']}, {item['name']},{item['quantity']},{item['price']}\n")
    except Exception as e:
        print(f"❌ Error saving inventory: {e}")


def generate_new_id(inventory):
    """Generate a new unique ID"""
    if not inventory:
        return 1
    max_id = max(item['id'] for item in inventory)
    return max_id + 1


def display_welcome():
    """Display welcome screen"""
    clear_screen()
    print("\n\n  INVENTORY MANAGEMENT SYSTEM")
    print("  -------------------------")
    print("  Simplify inventory tracking")
    print("  and reduce errors in stock records\n\n")
    input("  Press Enter to continue...")


def display_main_menu():
    """Display the main menu"""
    clear_screen()
    print("\nMAIN MENU")
    print("--------")
    print("1. Add New Item")
    print("2. View All Items")
    print("3. Search Item")
    print("4. Update Item")
    print("5. Delete Item")
    print("6. Adjust Stock (+/-)")
    print("7. Generate Reports")
    print("8. Credits")
    print("0. Exit")


def get_valid_input(prompt, input_type=str, allow_back=True):
    """Get validated user input with option to go back"""
    while True:
        user_input = input(prompt).strip()

        if allow_back and user_input == '0':
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
            print(f"Invalid input: {e}. Please try again.")


def add_item(inventory):
    """Add a new item to inventory"""
    clear_screen()
    print("ADD NEW ITEM")
    print("------------")

    print("\nID Options:")
    print("1. Auto-generate ID")
    print("2. Enter ID manually")
    print("0. Cancel")

    id_choice = get_valid_input("\nSelect ID option (1-2): ", int, allow_back=False)
    if id_choice is None or id_choice == 0:
        return

    if id_choice == 1:
        new_id = generate_new_id(inventory)
        # Check if ID exists (shouldn't happen with auto-increment, but just in case)
        while any(item['id'] == new_id for item in inventory):
            new_id += 1
        print(f"\nAuto-generated ID: {new_id}")
    elif id_choice == 2:
        new_id = get_valid_input("Enter ID: ", int)
        if new_id is None:
            return
        if any(item['id'] == new_id for item in inventory):
            print(f"ID {new_id} already exists. Please choose another.")
            input("\nPress Enter to continue...")
            return
    else:
        print("Invalid option.")
        input("\nPress Enter to continue...")
        return

    name = get_valid_input("\nEnter Item Name (press '0' to cancel): ", str)
    if name is None:
        return

    quantity = get_valid_input("Enter Quantity: ", int)
    if quantity is None:
        return

    price = get_valid_input("Enter Price (₱): ", float)
    if price is None:
        return

    inventory.append({
        'id': new_id,
        'name': name,
        'quantity': quantity,
        'price': price
    })

    save_inventory(inventory)
    print(f"\nSuccess! Item '{name}' (ID: {new_id}) added.")
    input("\nPress Enter to continue...")


def view_all_items(inventory):
    """Display all items in inventory"""
    clear_screen()
    print("CURRENT INVENTORY")
    print("----------------")

    if not inventory:
        print("\nNo items in inventory")
    else:
        print("\nID    Name                 Qty    Price")
        print("--------------------------------------")
        for item in inventory:
            print(f"{item['id']:<5} {item['name'][:18]:<18} {item['quantity']:>5}   ₱{item['price']:>7.2f}")

    input("\nPress Enter to return to menu...")


def search_item(inventory):
    """Search for items by ID or name"""
    clear_screen()
    print("SEARCH ITEM")
    print("-----------")

    search_term = get_valid_input("\nEnter ID or Name to search (press '0' to cancel): ", str)
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
    print("SEARCH RESULTS")
    print("-------------")

    if not results:
        print("\nNo matching items found")
    else:
        print("\nID    Name                 Qty    Price")
        print("--------------------------------------")
        for item in results:
            print(f"{item['id']:<5} {item['name'][:18]:<18} {item['quantity']:>5}   ₱{item['price']:>7.2f}")

    input("\nPress Enter to return to menu...")


def find_item_by_id_or_name(inventory, prompt):
    """Find item by ID or name with given prompt"""
    search_term = get_valid_input(prompt, str)
    if search_term is None:
        return None

    try:
        # Try searching by ID first
        search_id = int(search_term)
        item = next((i for i in inventory if i['id'] == search_id), None)
        if item:
            return item
    except ValueError:
        pass

    # Search by name if ID not found or not numeric
    matches = [i for i in inventory if search_term.lower() in i['name'].lower()]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print("\nMultiple matching items found:")
        for i, match in enumerate(matches, 1):
            print(f"{i}. {match['name']} (ID: {match['id']})")
        choice = get_valid_input("\nEnter number to select (press '0' to cancel): ", int)
        if choice is None or choice < 1 or choice > len(matches):
            return None
        return matches[choice - 1]

    print("\nItem not found")
    input("\nPress Enter to continue...")
    return None


def update_item(inventory):
    """Update item details"""
    clear_screen()
    print("UPDATE ITEM")
    print("-----------")

    item = find_item_by_id_or_name(inventory, "\nEnter ID or Name to update (press '0' to cancel): ")
    if not item:
        return

    print(f"\nCurrent Details for {item['name']} (ID: {item['id']}):")
    print(f"1. Name: {item['name']}")
    print(f"2. Quantity: {item['quantity']}")
    print(f"3. Price: ₱{item['price']:.2f}")

    field = get_valid_input("\nEnter number of field to update (1-3) or '0' to cancel: ", int)
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
        new_price = get_valid_input(f"Enter new price (current: ₱{item['price']:.2f}): ₱", float)
        if new_price is not None:
            item['price'] = new_price
    else:
        print("Invalid field selection.")
        input("\nPress Enter to continue...")
        return

    save_inventory(inventory)
    print("\nItem updated successfully!")
    input("\nPress Enter to continue...")


def delete_item(inventory):
    """Delete an item from inventory"""
    clear_screen()
    print("DELETE ITEM")
    print("-----------")

    item = find_item_by_id_or_name(inventory, "\nEnter ID or Name to delete (press '0' to cancel): ")
    if not item:
        return

    confirm = input(f"\nAre you sure you want to delete '{item['name']}' (ID: {item['id']})? (Y/N): ").strip().lower()
    if confirm == 'y':
        inventory[:] = [i for i in inventory if i['id'] != item['id']]
        save_inventory(inventory)
        print("\nItem deleted successfully!")
    else:
        print("\nDeletion cancelled.")

    input("\nPress Enter to continue...")


def adjust_stock(inventory):
    """Add or remove stock quantity"""
    clear_screen()
    print("ADJUST STOCK")
    print("------------")

    item = find_item_by_id_or_name(inventory, "\nEnter ID or Name to adjust (press '0' to cancel): ")
    if not item:
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
                print("Error: Resulting quantity cannot be negative.")
                input("\nPress Enter to continue...")
                return

            item['quantity'] = new_quantity
            save_inventory(inventory)
            print(f"\nStock updated. New quantity: {new_quantity}")
        else:
            print("Invalid input. Please use + or - before the number.")
    except ValueError:
        print("Invalid input. Please enter a valid number after + or -.")

    input("\nPress Enter to continue...")


def generate_reports(inventory):
    """Generate inventory reports"""
    clear_screen()
    print("INVENTORY REPORTS")
    print("----------------")
    print("\n1. Low Stock Alert")
    print("2. Total Inventory Value")
    print("0. Back to Main Menu")

    choice = get_valid_input("\nSelect report option (1-2): ", int, allow_back=False)

    if choice == 1:
        # Low stock report
        low_stock = [item for item in inventory if item['quantity'] < MIN_STOCK_ALERT]

        clear_screen()
        print("LOW STOCK ALERT")
        print("--------------")

        if not low_stock:
            print("\nNo items below stock threshold (10)")
        else:
            print(f"\nItems below {MIN_STOCK_ALERT} units:")
            print("\nID    Name                 Qty    Price")
            print("--------------------------------------")
            for item in low_stock:
                print(f"{item['id']:<5} {item['name'][:18]:<18} {item['quantity']:>5}   ₱{item['price']:>7.2f}")

        input("\nPress Enter to continue...")

    elif choice == 2:
        # Total inventory value
        total_value = sum(item['quantity'] * item['price'] for item in inventory)

        clear_screen()
        print("TOTAL INVENTORY VALUE")
        print("---------------------")
        print(f"\nTotal Value: ₱{total_value:,.2f}")
        input("\nPress Enter to continue...")

    elif choice == 0:
        return


def show_credits():
    """Display credits screen"""
    clear_screen()
    print("CREDITS")
    print("-------")
    print("\nLead Programmer:")
    print("Daniel Udasco")
    print("GitHub: https://github.com/danieldan64/")

    print("\nUX Designer & QA Engineer:")
    print("Hazel Mae Jalandoni")
    print("GitHub: https://github.com/hnutcelest")

    input("\nPress Enter to return to menu...")


def main():
    """Main program loop"""
    initialize_inventory_file()
    inventory = load_inventory()

    display_welcome()

    while True:
        display_main_menu()
        choice = get_valid_input("\nSelect an option (0-8): ", int, allow_back=False)

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
            show_credits()
        elif choice == 0:
            print("\nThank you for using the Inventory Management System!")
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select 0-8.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()