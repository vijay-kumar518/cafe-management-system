import json

MENU_FILE = "menu.json"
ORDERS_FILE = "orders.json"

# Load/Save helpers
def load_file(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_file(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# input validation functions
def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("❌ Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input. Enter a number.")

def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("❌ Please enter a positive integer.")
                continue
            return value
        except ValueError:
            print("❌ Invalid input. Enter an integer.")

def add_item():
    menu = load_file(MENU_FILE)
    while True:
        item = input("Enter Item Name: ").strip().capitalize()
        if item == "":
            print("❌ Item name cannot be empty.")
            continue
        if item in menu:
            print("❌ Item already exists in menu.")
            continue
        break

    price = get_valid_float("Enter Price: ₹")
    menu[item] = price
    save_file(MENU_FILE, menu)
    print("✅ Item Added Successfully!\n")

def view_menu():
    menu = load_file(MENU_FILE)
    if not menu:
        print("No items in menu.\n")
    else:
        print("\n--- Cafe Menu ---")
        for item, price in menu.items():
            print(f"{item}: ₹{price}")
        print()

def remove_or_update_item():
    menu = load_file(MENU_FILE)
    if not menu:
        print("Menu is empty!\n")
        return

    view_menu()
    choice = input("Enter item name to remove/update: ").capitalize()
    if choice in menu:
        action = input("Type 'remove' to delete or 'update' to change price: ").lower()
        if action == "remove":
            menu.pop(choice)
            save_file(MENU_FILE, menu)
            print(f"✅ {choice} removed successfully.\n")
        elif action == "update":
            new_price = get_valid_float(f"Enter new price for {choice}: ₹")
            menu[choice] = new_price
            save_file(MENU_FILE, menu)
            print(f"✅ {choice} updated successfully.\n")
        else:
            print("❌ Invalid action.\n")
    else:
        print("❌ Item not found.\n")

def take_order():
    menu = load_file(MENU_FILE)
    if not menu:
        print("No items available. Please add items first.\n")
        return
    
    student_name = input("Enter Student Name: ").strip().title()
    if student_name == "":
        student_name = "Unknown"

    order = []
    total = 0
    while True:
        view_menu()
        item = input("Enter item to order (or 'done' to finish): ").capitalize()
        if item.lower() == "done":
            break
        if item in menu:
            qty = get_valid_int(f"Enter quantity of {item}: ")
            cost = menu[item] * qty
            order.append({"item": item, "qty": qty, "cost": cost})
            total += cost
        else:
            print("❌ Item not in menu.")
    
    if order:
        orders = load_file(ORDERS_FILE)
        if not isinstance(orders, list):  # initialize if empty
            orders = []
        orders.append({"student": student_name, "order": order, "total": total})
        save_file(ORDERS_FILE, orders)
        print(f"\n✅ Order Placed for {student_name}! Total Bill: ₹{total}\n")

def view_orders():
    orders = load_file(ORDERS_FILE)
    if not orders:
        print("No orders yet.\n")
    else:
        print("\n--- All Orders ---")
        for i, o in enumerate(orders, 1):
            print(f"\nOrder {i} - Student: {o.get('student', 'Unknown')}")
            for item in o["order"]:
                print(f"{item['item']} x {item['qty']} = ₹{item['cost']}")
            print(f"Total: ₹{o['total']}")
        print()

def cafe_menu():
    while True:
        print("====== Cafe Management System ======")
        print("1. Add Item to Menu")
        print("2. View Menu")
        print("3. Take Order")
        print("4. View Orders")
        print("5. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            add_item()
        elif choice == "2":
            view_menu()
        elif choice == "3":
            take_order()
        elif choice == "4":
            view_orders()
        elif choice == "5":
            break
        else:
            print("Invalid choice!\n")

# Run Cafe System
cafe_menu()