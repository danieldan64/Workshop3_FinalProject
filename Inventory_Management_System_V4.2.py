import os

#FILE HANDLING SECTION--------------
file_path = r"C:\Users\DanielUdasco\Desktop\Workshop3_FinalProject\inventory_data\inventory.txt"

#CREATE inventory.txt if it doesn't exist
def initialize_inventory_file():
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # just create an empty file

#LOAD items from inventory.txt (for functions like View_all_items)
def load_inventory():
    items = []
    if not os.path.exists(file_path):
        return items
    with open(file_path, 'r') as file:
        lines = file.readlines()[4:]
        for line in lines:
            parts = line.strip().split("|")
            if len(parts) == 2:
                left_part = parts[0].strip()
                price = parts[1].split()
                id_name_qty = left_part.split()

                if len(id_name_qty) >=3:
                    name_qty = "".join(id_name_qty[1:])
                    name_qty = name_qty.rsplit("",1)
                    items.append({
                    "name": name.strip(),
                    "qty": qty.strip(),
                    "status": status.strip()
                })
    return items

#SAVE items from inventory.txt (for functions later on)
def save_inventory(items):
    with open(file_path, 'w') as file:
        file.write("-------------------------------INVENTORY_MANAGEMENT_SYSTEM------------------------\n")
        file.write("=" 85 + "\n")
        file.write(file"{'ID.':<5}{'Name'}:<50}{'Quantity':<15} | Price\n")
        file.write("-" * 85 + "\n")
        for i, act in enumerate(items, 1):
            file.write(file"{i:<5}{act['name']:<50}{act['qty']:<15} | {act['price']}\n")

def append_items_to_file(item, index):
    with open(path, "a") as file:
        file.write(f"{index:<5}{item['name']:<50}{item}['qty']:<15} }| {activity['price']}\n")
#END OF FILE HANDLING SECTION-------------

# Generate ID (unique to each other)
def generate_new_id(inventory):
    if not inventory:
        return 1
    max_id = max(item['id'] for item in inventory)
    return max_id + 1

# Welcome Screen (open just once when opening the IMS.py)
def display_welcome():
    print("\n\n  INVENTORY MANAGEMENT SYSTEM")
    print("  -------------------------")
    print("  Simplify inventory tracking")
    print("  and reduce errors in stock records\n\n")
    input("  Press Enter to continue...")

# Display Main Menu Screen
def display_main_menu():
    print("\nMAIN MENU")
    print("--------")
    print("1. Add New Item")
    print("2. View All Items")
    print("3. Search Item")
    print("4. Update Item")
    print("5. Delete Item")
    print("6. Adjust Stock (+/-)")
    print("7. Credits")
    print("0. Exit")

# Only get valid input from users (to avoid errors) with option to go back (press '0') (Back button in console)
def get_valid_input(prompt, input_type=str, allow_back=True):
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

# Add item to inventory.txt
def add_item(inventory):
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
        new_id = generate_new_id(inventory) #Check if already ID exist, if not increment to 1
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

# Display all items in inventory.txt
def view_all_items(inventory):
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

# Search for item by name or ID
def search_item(inventory):
    print("SEARCH ITEM")
    print("-----------")

    search_term = get_valid_input("\nEnter ID or Name to search (press '0' to cancel): ", str)
    if search_term is None:
        return
    results = []
    try:
        search_id = int(search_term)
        results = [item for item in inventory if item['id'] == search_id]
    except ValueError:
        # Search by name if ID not found
        results = [item for item in inventory if search_term.lower() in item['name'].lower()]
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

#Find item by name or ID (For delete, update, adjust item functions)
def find_item_by_id_or_name(inventory, prompt):
    search_term = get_valid_input(prompt, str)
    if search_term is None:
        return None
    try:
        search_id = int(search_term)
        item = next((i for i in inventory if i['id'] == search_id), None)
        if item:
            return item
    except ValueError:
        pass
    # Search by name if ID not found
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

# Update item info
def update_item(inventory):
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


# Delete Items from inventory.txt
def delete_item(inventory):
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

# Add or Subtract Stock (for quick inventory restocking)
def adjust_stock(inventory):
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
        # if '+' add... if '-' subtract stock
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

# Display credits (w/ github links)
def show_credits():
    """Display credits screen"""
    print("CREDITS")
    print("-------")
    print("\nLead Programmer:")
    print("Daniel Udasco")
    print("GitHub: https://github.com/danieldan64/")
    print("\nUX Designer & QA Engineer:")
    print("Hazel Mae Jalandoni")
    print("GitHub: https://github.com/hnutcelest")
    input("\nPress Enter to return to menu...")

#Main
def main():
    initialize_inventory_file()
    inventory = load_inventory()
    display_welcome()

    #Loop
    while True:
        display_main_menu()
        choice = get_valid_input("\nSelect an option (0-7): ", int, allow_back=False)

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
            show_credits()
        elif choice == 0:
            print("\nThank you for using the Inventory Management System!")
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select 0-7.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()