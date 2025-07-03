def clear_screen():
    for _ in range(3):
        print("\n")

def user_list():
    users = []  # Use a list to store user details
    with open("user_data.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            email, password, firstname, lastname, role, role_id, new_user_id = line.strip().split(',', 6)
            users.append((new_user_id, firstname, lastname, email, role, role_id))  
    return users

def view_user_list(role_id, user_id, users):
    print(f"{'User ID':<8} {'Firstname':<15} {'Lastname':<15} {'Email':<25} {'Role':<10} {'Role ID':<10}")
    for user in users:
        new_user_id, firstname, lastname, email, role, roleid = user
        print(f"{new_user_id:<8} {firstname:<15} {lastname:<15} {email:<25} {role:<10} {roleid}")
    return system_administration(role_id, user_id)

def manage_access_main(role_id, user_id):
    clear_screen()
    print("\nSelect an option:")
    print("i. Modify user accessibility")
    print("ii. Add Role ID")
    print("iii.Quit from Manage Access")
    choice = input("ENTER A CHOICE: ")
    if choice == "i":
        modify_accessibility()
    elif choice == "ii":
        add_role_id()
    elif choice == "iii":
        print("Exiting from Manage Access...\n")
        return system_administration(role_id, user_id)
    else:
        print("Invalid option\n")
    return manage_access_main(role_id, user_id)

def modify_accessibility():
    user_id = input("Enter user_id to modify accessibility (it will remove access and return back as customer): ")
    found = False 
    update_lines = []
    
    with open("user_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 7 and data[6] == user_id:  
                print(f"Current Role ID: {data[4]}")
                data[4] = 'customer'  
                data[5] = '0'         
                found = True
            update_lines.append(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]}\n")
    
    if found:
        with open("user_data.txt", "w") as file:
            file.writelines(update_lines)
            print("User role updated.")  
    else:
        print("No user data found to update.")

def max_custom(initial_value, last_role_id):
    if initial_value > last_role_id:
        return initial_value
    else:
        return last_role_id

def add_role_id(): 
    with open("user_roles.txt", "r") as file:
        roles = [line.strip().split(",") for line in file]

    # Group the roles by their name (in lowercase) and extract their IDs
    role_id = {
        "manager": [int(role_details[0][2:]) for role_details in roles if role_details[1].lower() == "manager"],
        "cashier": [int(role_details[0][2:]) for role_details in roles if role_details[1].lower() == "cashier"],
        "baker": [int(role_details[0][2:]) for role_details in roles if role_details[1].lower() == "baker"]
    }

    role_to_add = input("Enter the role that you would like to add (manager/cashier/baker): ").lower()
    
    if role_to_add not in role_id:
        print("Invalid role entered!")
        return

    quantity_to_add = int(input(f"How many {role_to_add}(s) would you like to add? "))

    # Get the last ID for the selected role
    if role_id[role_to_add]:
        last_id = 0
        for id in role_id[role_to_add]:
            last_id = max_custom(last_id, id)  # Get the current maximum ID for the role
    else:
        last_id = 0  # No existing roles found, start from 0

    # Use max_custom to determine the maximum ID
    last_id = max_custom(last_id, 0)  # Ensure we have a valid last_id

    # Generate new role IDs
    new_roles = []
    for i in range(1, quantity_to_add + 1):
        new_id = f"{role_to_add[:2].upper()}{last_id + i:02d}"  # Role ID format
        new_roles.append(f"{new_id},{role_to_add}")  # Keep everything in lowercase
    
    # Check if the new IDs already exist in the file
    existing_lines = set(",".join(role) for role in roles)  # Create a set of existing lines to check for duplicates
    updated_roles = []

    for role in new_roles:
        if role not in existing_lines:
            updated_roles.append(role)  # Only append if it's not already in the file

    # Append the new roles to the file only if there are new roles
    if updated_roles:
        with open("user_roles.txt", "a") as file:
            for role in updated_roles:
                file.write(role + "\n")
        print(f"Successfully added {len(updated_roles)} new {role_to_add}(s).")
    else:
        print("No new roles to add. All roles already exist.")

def delete_user_account(role_id, user_id):
    delete_user_id = input("Enter user ID to delete: ")
    updated_lines = []
    found = False

    with open("user_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 6 and delete_user_id == data[6]:
                found = True
                print(f"Are you sure you would like to delete this item: {data[4]} - {data[2]}")
                delete_product = input("Please enter yes or no (yes/no): ").lower()
                
                if delete_product == "yes":
                    print("User deleted successfully.")
                else:
                    print("Deletion cancelled.")
                    return system_administration(role_id, user_id)                
            else:
                updated_lines.append(line)

    if found:
        with open("user_data.txt", "w") as file:
            file.writelines(updated_lines)
    else:
        print("User ID not found.")
    return system_administration(role_id, user_id)

def system_administration(role_id, user_id):
    clear_screen()
    print("-----System Administration-----")
    print("1. User List Overview")
    print("2. Manage Access")
    print("3. Remove User Acoount")
    print("4. Exit System Administration")
    choice = input("ENTER A CHOICE: ")
    
    if choice == "1":
        users = user_list()
        view_user_list(role_id, user_id, users)
    elif choice == "2":
        manage_access_main(role_id, user_id)
    elif choice == "3":
        delete_user_account(role_id, user_id)
    elif choice == "4":
        print("Exiting System Administration...")
        manager_main(role_id, user_id)  
        return
    else:
        print("Invalid option")
        return system_administration(role_id, user_id)

def order_list():
    orders = []  
    with open("orders.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            order_id, cart_id, product_id, item_name, quantity, total_price, user_id, status, payment_method, current_datetime = line.strip().split(',', 9)
            orders.append((order_id, cart_id, product_id, item_name, quantity, total_price, user_id, status, payment_method, current_datetime))  # Append user details as a tuple
    return orders

def display_order_list(role_id, user_id):
    orders = order_list()
    print(f"\n{'Order ID':<10} {'User ID':<10} {'Product ID':<10} {'Item':<30} {'Qty':<10} {'Status':<15} {'Time':<10}")
    for order in orders:
        order_id, cart_id, product_id, item_name, quantity, total_price, user_id, status, payment_method, current_datetime = order
        print(f"{order_id:<10} {user_id:<10} {product_id:<10} {item_name:<30} {quantity:<10} {status:<15}{current_datetime}")
    return manager_main(role_id, user_id)

def read_ingredient_list():
    ingredient = {}
    with open("ingredient.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            ingredient_id, name, net_weight, stock, unit_price, current_weight_left = line.strip().split(',', 5)  
            ingredient[ingredient_id] = (name, net_weight, int(stock), float(unit_price), int(current_weight_left))  
    return ingredient

def display_ingredient(ingredients, role_id, user_id):
    print(f"{'ID':<10} {'Ingredient Name':<30} {'Net Weight':<15} {'Stock':<8} {'Unit Price':<15}")
    for ingredient_id, (name, net_weight, stock, unit_price, current_weight_left) in ingredients.items():
        print(f"{ingredient_id:<10} {name:<30} {net_weight:<15} {stock:<8} RM{unit_price:.2f}")
    return 

def restock_record(role_id, user_id):
    # Display ingredient list
    restock_ingredient_id = input("Enter ingredient id to restock: ").strip().upper()
    ingredients = read_ingredient_list()  
    ingredient_found = False
    ingredient_name = ""
    current_stock = 0  

    for ingredient_id, details in ingredients.items():  
        if ingredient_id == restock_ingredient_id:  
            ingredient_name = details[0]  
            current_stock = details[2]  
            ingredient_found = True
            break  

    if not ingredient_found:
        print(f"Ingredient ID {restock_ingredient_id} not found in ingredient list.\n")
        return inventory_control(role_id, user_id)
    
    print(f"Current Stock Quantity: {current_stock}")

    try:
        restock_amount = int(input(f"Enter the total quantity of {ingredient_name} to restock: ").strip())

        new_stock = current_stock + restock_amount
        print(f"New Stock Quantity for {ingredient_name}: {new_stock}")

    except ValueError:
        print("Error: Please enter a valid number for the quantity.")
        return inventory_control(role_id, user_id)

    updated_lines = []
    with open("ingredient.txt","r")as file:
        lines = file.readlines()
    for line in lines:
        data = line.strip().split(',')
        if data[0] == restock_ingredient_id:
            # Update the stock quantity
            data[3] = str(new_stock)  
            
            # Extract numeric value 
            numeric_stock_value, unit = extract_numeric_value_and_unit(data[2])
            
            data[5] = str(int(numeric_stock_value * float(data[3])))  

            updated_line = ','.join(data)
            updated_lines.append(updated_line + '\n')
        else:
            updated_lines.append(line)

    with open("ingredient.txt", "w") as file:
        file.writelines(updated_lines)

    print("Stock updated successfully.")
    return inventory_control(role_id, user_id)

def extract_numeric_value_and_unit(quantity):
    """Extracts the numeric value and unit from a quantity string."""
    numeric_value = ""
    unit = ""

    # Ensure quantity is a string before iterating
    quantity_str = str(quantity)

    # Loop through each character to separate the numeric part and unit
    for char in quantity_str:
        if char.isdigit() or char == '.':  # Handle numbers and decimal points
            numeric_value += char
        else:
            unit += char  # Once non-digit is found, it is considered part of the unit

    numeric_value = float(numeric_value) if numeric_value else 0.0
    unit = unit.strip()  # Clean up any surrounding spaces

    return numeric_value, unit

def opening_ingredient_stock_record(role_id, user_id):
    ingredients = read_ingredient_list()
    display_ingredient(ingredients, role_id, user_id)
    try:
        with open("opening_ingredient_stock.txt", "r") as file:
            existing_records = file.readlines()
    except FileNotFoundError:
        existing_records = []

    existing_stock = {}
    for record in existing_records:
        data = record.strip().split(",")
        if len(data) == 6:
            existing_stock[data[0]] = record  

    try:
        with open("ingredient.txt", "r") as file:
            ingredient_data = file.readlines()
    except FileNotFoundError:
        print("Your ingredient list is empty.")
        return

    opening_ingredient_record = input("Enter would you like to record ingredient stock of the day (yes/no): ").strip().lower()
    if opening_ingredient_record != "yes":
        return inventory_control(role_id, user_id)

    # Update or add records in the opening_ingredient_stock.txt
    with open("opening_ingredient_stock.txt", "w") as file:
        for ingredient_item in ingredient_data:
            ingredient_data = ingredient_item.strip().split(",")
            if len(ingredient_data) == 6:
                ingredient_id, name, net_weight, stock, unit_price, current_weight_left = ingredient_data
                
                # If the ingredient_id exists, update the record
                if ingredient_id in existing_stock:
                    existing_stock[ingredient_id] = f"{ingredient_id},{name},{net_weight},{stock},{unit_price},{current_weight_left}\n"
                else:
                    existing_stock[ingredient_id] = f"{ingredient_id},{name},{net_weight},{stock},{unit_price},{current_weight_left}\n"
        
        # Write all updated records back to opening_ingredient_stock.txt
        for record in existing_stock.values():
            file.write(record)

    print("Opening ingredient stock has been recorded and updated successfully.")
    return inventory_control(role_id, user_id)

def product_list():
    menu = {}
    with open("product_menu.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            category, product_id, item, price, discount, discount_price, item_stock = line.strip().split(',', 6)
            if category not in menu:
                menu[category] = []
            menu[category].append((product_id, item, float(price), int(discount), float(discount_price), int(item_stock)))
    return menu

def wastage_record(role_id, user_id):
    print("------------------------------------------------------------------------")
    print("All products that have reached their expiration date are recorded as waste.\nPlease ensure that the quantity of such items is accurately recorded.")
    print("------------------------------------------------------------------------")
    wastage_product_id = input("Enter wastage product id: ")
    products = product_list()
    product_found = False
    product_name = ""
    current_stock = 0  

    # Search for the product in the product_list
    for category, product_details in products.items():
        for product_detail in product_details:
            if product_detail[0] == wastage_product_id:  # product_id is at index 0
                product_name = product_detail[1]  # product name is at index 1
                current_stock = product_detail[5]  # stock is at index 5
                product_found = True
                break
        if product_found:
            break

    if not product_found:
        print(f"Product ID {wastage_product_id} not found in product list.\n")
        return inventory_control(role_id, user_id)
    
    print(f"Current Stock Quantity: {current_stock}")

    try:
        wastage_amount = int(input(f"Enter the total quantity of wastage for {product_name}: ").strip())

        if wastage_amount > current_stock:
            print("Error: Wastage amount cannot be greater than current stock.")
            return inventory_control(role_id, user_id)

        new_stock = current_stock - wastage_amount
        print(f"New Stock Quantity Left for {product_name}: {new_stock}")

    except ValueError:
        print("Error: Please enter a valid number for the quantity.")
        return inventory_control(role_id, user_id)

    # Update product stock in product_menu.txt
    updated_lines = []
    with open("product_menu.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        data = line.strip().split(',')
        if data[1] == wastage_product_id:  # product_id is at index 1 in file
            data[6] = str(new_stock)  # item_stock is at index 6

            updated_line = ','.join(data)
            updated_lines.append(updated_line + '\n')
            save_wastage_record(line, wastage_amount)
        else:
            updated_lines.append(line)

    with open("product_menu.txt", "w") as file:
        file.writelines(updated_lines)
    
    print("Wastage removed. Stock updated successfully.")
    return inventory_control(role_id, user_id)

from datetime import datetime

def save_wastage_record(product_line, wastage_amount):
    # Split the product line and replace stock with wastage amount
    data = product_line.strip().split(',')
    data[6] = str(wastage_amount)  # Replace stock with wastage amount

    # Get the current date and time in the format YYYY-MM-DD HH:MM:SS
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a formatted line for wastage_record.txt with the timestamp
    wastage_record_line = ','.join(data) + f",{current_time}"

    try:
        # Append the line to wastage_record.txt
        with open("wastage_record.txt", "a") as wastage_file:
            wastage_file.write(wastage_record_line + '\n')

        print(f"Wastage record saved for product ID {data[1]} with quantity {wastage_amount} at {current_time}.")
    
    except FileNotFoundError:
        print("Error: The file 'wastage_record.txt' was not found.")
        # Create the file if it doesn't exist
        try:
            with open("wastage_record.txt", "w") as wastage_file:  # Create the file if not found
                wastage_file.write(wastage_record_line + '\n')
            print(f"Wastage record file created and saved for product ID {data[1]} with quantity {wastage_amount} at {current_time}.")
        except Exception as e:
            print(f"An unexpected error occurred while trying to create the file: {e}")

def display_malfunction_equipment(equipment):
    print(f"\n{'ID':<10} {'Equipment Name':<30} {'Functionality':<70} {'Availability':<12}")
    for equipment_id, items in equipment.items():
        for item in items:
            name, functionality, availability, notes = item[1], item[2], item[3], item[4]
            if notes != '0':
                print(f"{equipment_id:<10} {name:<30} {functionality:<70} {availability:<12} {notes}")
            else:
                break
    return 

def equipment_list():
        equipment = {}
        with open("equipment.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                equipment_id,name,functionality,availability,notes = line.strip().split(',', 4)  
                if equipment_id not in equipment:
                    equipment[equipment_id] = []
                equipment[equipment_id].append((equipment_id,name,functionality,availability,notes))
        return equipment

def equipment_maintenance(role_id, user_id):
    equipment = equipment_list() 
    display_malfunction_equipment(equipment)
    
    eqp_maintenance_id = input("Enter Equipment ID that had maintenance (0 to cancel): ")
    if eqp_maintenance_id == '0':
        return inventory_control(role_id, user_id)
    equipment_exists = False
    with open("equipment.txt", "r") as file:
        lines = file.readlines()
    updated_lines = []

    for line in lines:
        data = line.strip().split(",")
        if eqp_maintenance_id == data[0]:  
            equipment_exists = True
            user_input = input(f"Would you like to update {data[1]}'s availability (yes/no): ")
            
            if user_input.lower() != 'yes':
                print("Cancel update maintenance status.")
                return inventory_control(role_id, user_id)
            data[3] = 'available'
            data[4] = '0'
            updated_line = ",".join(data) + "\n"
            updated_lines.append(updated_line)  
        else:
            updated_lines.append(line)  

    if equipment_exists:
        with open("equipment.txt", "w") as file:
            file.writelines(updated_lines)
        print(f"Updated equipment ID {eqp_maintenance_id} maintenance status.")
    else:
        print(f"Equipment ID {eqp_maintenance_id} not found.")
    return inventory_control(role_id, user_id)

def inventory_control(role_id, user_id):
    clear_screen()
    print("-----Inventory Control-----")
    print("1. Opening Ingredient Stock Record")
    print("2. Restock Record")
    print("3. Wastage Record")
    print("4. Equipment Maintanence")
    print("5. Exit Inventory Control")
    choice = input("ENTER A CHOICE: ")
    if choice == "1":
        opening_ingredient_stock_record(role_id, user_id)
    elif choice == "2":
        restock_record(role_id, user_id)
    elif choice == "3":
        wastage_record(role_id, user_id)
    elif choice == "4":
        equipment_maintenance(role_id, user_id)
    elif choice == "5":
        print("Exiting Inventory Control...")
        return manager_main(role_id, user_id)
    else:
        print("Invalid option")
        return inventory_control(role_id, user_id)

def ingredient_cost():
    ingredients = read_ingredient_list()
    total_production_cost = 0
    for ingredient_id, details in ingredients.items():
        name, net_weight, stock, unit_price, current_weight_left = details
        production_cost = float(unit_price) * int(stock)
        total_production_cost += production_cost
    print(f"\nTotal Production Cost from ingredient.txt: RM{total_production_cost:.2f}")

    total_production_cost_opening = 0
    try:
        with open("opening_ingredient_stock.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                ingredient_id, name, net_weight, stock, unit_price, current_weight_left = line.strip().split(',', 5)
                production_cost_opening = float(unit_price) * int(stock)
                total_production_cost_opening += production_cost_opening

            print(f"\nTotal Production Cost from opening_ingredient_stock.txt: RM{total_production_cost_opening:.2f}")

    except FileNotFoundError:
        print("opening_ingredient_stock.txt not found.")

    total_ingredient_cost = total_production_cost_opening - total_production_cost
    print(f"Total ingredient cost: RM{total_ingredient_cost:.2f}")
    return total_ingredient_cost

def product_sales_cost(total_expenses):
    total_sales = 0

    with open("sales_record.txt", "r") as file:
        lines = file.readlines()

        if lines:
            last_line = lines[-1]
            current_datetime, total_items_sold, sales, role_id = last_line.strip().split(',', 3)
            total_sales = float(sales)

    # Calculate net profit or loss
    net_profit = total_sales - total_expenses
    
    # Display profit or loss based on the net result
    if net_profit > 0:
        print(f"It is a profit: RM{net_profit:.2f}")
    else:
        print(f"It is a loss: RM{-net_profit:.2f}")

    return total_sales, net_profit

def generate_z_report(role_id, user_id):
    total_ingredient_cost = ingredient_cost()  # Calculate ingredient costs
    total_wastage_cost = 0  # Initialize total wastage cost

    # Get the current date and time
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")

    # Calculate total wastage costs
    with open("wastage_record.txt", "r") as file:
        for line in file:
            category, product_id, item, price, discount, discount_price, wastage_amount, timestamp = line.strip().split(',')
            wastage_date = timestamp.split(" ")[0]
        
            if wastage_date == current_date:  # Now current_date is defined
                wastage_amount = int(wastage_amount)
                price = float(price)
                discount_price = float(discount_price)
                discount = int(discount)

                # Use discount price if the item has a discount
                item_price = discount_price if discount > 0 else price
                total_wastage_cost += wastage_amount * item_price

    # Calculate total expenses after wastage cost is determined
    total_expenses = total_ingredient_cost + total_wastage_cost  # Ensure this is calculated correctly
    print(f"Total Wastage Cost: RM{total_wastage_cost:.2f}")
    print(f"Total Expenses: RM{total_expenses:.2f}")  # Print total expenses for debugging
    
    total_sales, net_profit = product_sales_cost(total_expenses)  # Call to calculate profit/loss

    orders = {}
    product_sales = {}
    total_items_sold = 0
    total_orders = 0
    total_sales = 0.0
    total_credit_sales = 0.0
    total_e_wallet_sales = 0.0

    # Read original stock data
    original_stock = {}
    with open("production_record.txt", "r") as file:
        for line in file:
            production_id, time, product_id, product_name, quantity, baker_id, notes, expiration_date = line.strip().split(",")
            quantity = int(quantity)
            if product_id not in original_stock:
                original_stock[product_id] = 0
            original_stock[product_id] += quantity

    # Read current item stock from product_menu.txt
    current_stock = {}
    with open("product_menu.txt", "r") as file:
        for line in file:
            category, product_id, product_name, price, discount, discounted_price, stock = line.strip().split(",")
            current_stock[product_id] = {
                'name': product_name,
                'price': float(price),
                'stock': int(stock)
            }

    current_time = current_datetime.strftime("%H:%M")
    
    # Read orders from orders.txt
    with open("orders.txt", "r") as file:
        for line in file:
            order_id, cart_id, product_id, product_name, quantity, total_price, user_id, status, payment_method, timestamp = line.strip().split(",")
            order_date = timestamp.split(" ")[0]
            
            if order_date == current_date:
                quantity = int(quantity)
                total_price = float(total_price)

                # Track total items sold
                total_items_sold += quantity
            
                # Track total number of orders
                if order_id not in orders:
                    total_orders += 1
                    orders[order_id] = 0
            
                # Track sales by product and aggregate data
                if product_id not in product_sales:
                    product_sales[product_id] = {
                        'name': product_name,
                        'quantity': 0,
                        'total_price': 0.0
                    }
                product_sales[product_id]['quantity'] += quantity
                product_sales[product_id]['total_price'] += total_price

                # Track payment method totals
                if payment_method.lower() == "e-wallet":
                    total_e_wallet_sales += total_price
                else:
                    total_credit_sales += total_price  
    
    # Total sales and expenses
    total_sales = total_credit_sales + total_e_wallet_sales

    print("\n***If there appears to be any errors in the item sales report, please verify whether the previous day's closing was completed properly.***\n")

    print("------------------------------------------------------------------------")
    print("                               Z Report")
    print("------------------------------------------------------------------------")
    print(f"Bakery Name: KL Baguette")
    print(f"Date: {current_date}")
    print(f"Time: {current_time}")
    print(f"Manager ID: {role_id}")
    print("------------------------------------------------------------------------")
    print("[Income Overview]")
    print(f"{'Total Sales':<30}RM{total_sales:,.2f}")
    print(f"{'Total Credit Sales':<30}RM{total_credit_sales:,.2f}")
    print(f"{'Total E-Wallet Sales':<30}RM{total_e_wallet_sales:,.2f}")
    
    print("\n[Expenses Overview]")
    print(f"{'Total Expenses':<30}RM{total_expenses:,.2f}")

    print("\n[Profit & Loss Statement]")
    print(f"{'Net Sales':<30}RM{total_sales:,.2f}")
    
    # Only display either profit or loss based on net result
    if net_profit > 0:
        print(f"{'Profit':<30}RM{net_profit:,.2f}")
    else:
        print(f"{'Loss':<30}RM{-net_profit:,.2f}")
    
    print("------------------------------------------------------------------------")

    print("[Detailed Sales Breakdown]")
    print("------------------------------------------------------------------------")
    print(f"{'Item Name':<30}{'Item ID':<10}{'Quantity Sold':<15}{'Unit Price':<15}{'Total Sales'}")
    for product_id, data in product_sales.items():
        unit_price = data['total_price'] / data['quantity'] 
        print(f"{data['name']:<30}{product_id:<10}{data['quantity']:<15}RM{unit_price:>5,.2f}{' ':<8}RM{data['total_price']:>6,.2f}")

    print(f"\n{'Total':<30}{'':<10}{total_items_sold:<30}RM{total_sales:,.2f}")
    print("\n------------------------------------------------------------------------")
    print("[Payment Summary]")
    print("------------------------------------------------------------------------")
    print(f"{'Payment Method':<20}{'Amount'}")
    print(f"{'E-Wallet':<20}RM{total_e_wallet_sales:,.2f}")
    print(f"{'Debit/Credit Card':<20}RM{total_credit_sales:,.2f}")
    return manager_main(role_id, user_id)

def feedback_list():
    feedbacks = []  # Use a list to store user details
    with open("feedback.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            feedback_id, user_id, order_id, product_id, feedback = line.strip().split(',', 4)
            feedbacks.append((feedback_id, user_id, order_id, product_id, feedback))
    return feedbacks

def display_feedbak_list(role_id, user_id):
    feedbacks = feedback_list()
    print(f"\n{'Feedback ID':<15} {'User ID':<10} {'Order ID':<10} {'Product ID':<15} {'Feedback'}")
    for feedback_detail in feedbacks:
        feedback_id, user_id, order_id, product_id, feedback = feedback_detail
        print(f"{feedback_id:<15} {user_id:<10} {order_id:<10} {product_id:<15} {feedback} ")
    return manager_main(role_id, user_id)

def account_management(role_id, user_id):
    while True:
        clear_screen()
        print("-----Manage Your Account-----")
        print("i. Edit First Name")
        print("ii. Edit Last Name")
        print("iii. Change Password")
        print("iv. Exit")
        choice = input("ENTER A CHOICE: ")

        if choice == "i":
            modify_firstname(role_id, user_id)
        elif choice == "ii":
            modify_lastname(role_id, user_id)
        elif choice == "iii":
            modify_password(role_id, user_id)
        elif choice == "iv":
            manager_main(role_id, user_id)
        else:
            print("Invalid option.")
            return account_management(role_id, user_id)

def modify_firstname(role_id, user_id):
    found = False
    update_lines = []

    with open("user_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 7 and data[6] == user_id:
                print(f"Current First Name: {data[2]}")
                new_firstname = input("Enter New First Name: ")
                data[2] = new_firstname
                found = True
            update_lines.append(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]}\n")

    if found:
        with open("user_data.txt", "w") as file:
            file.writelines(update_lines)
        print("First Name updated.")
    else:
        print("No user data found to update.")

def modify_lastname(role_id, user_id):
    found = False
    update_lines = []

    with open("user_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 7 and data[6] == user_id:
                print(f"Current Last Name: {data[3]}")
                new_lastname = input("Enter New Last Name: ")
                data[3] = new_lastname
                found = True
            update_lines.append(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]}\n")

    if found:
        with open("user_data.txt", "w") as file:
            file.writelines(update_lines)
        print("Last Name updated.")
    else:
        print("No user data found to update.")

def modify_password(role_id, user_id):
    new_password = input("Enter New Password: ")
    found = False
    update_lines = []

    if len(new_password) <= 8:
        print("Password is too short.")
        return

    new_confpassword = input("Confirm your password: ")
    if new_password != new_confpassword:
        print("Passwords do not match. Please try again.")
        return

    with open("user_data.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 7 and data[6] == user_id:
                data[1] = new_password
                found = True
            update_lines.append(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]}\n")

    if found:
        with open("user_data.txt", "w") as file:
            file.writelines(update_lines)
        print("Password updated.")
    else:
        print("No user data found to update.")

def manager_notice (role_id, user_id):
    print("-----------------------------------------------------")
    print("NOTICE: Opening Stock Report for Store Opening\n")
    print("To store manager,")
    print("Please ensure that you click the *Inventory Control - Opening Stock Report* button at the start of your shift to initialize the stock for the day.\nThis report is crucial for tracking inventory and ensuring total expenses.\n")
    print("Reminder:")
    print("The Opening Stock Report must be generated at the beginning of the store's opening procedures.")
    print("This step is critical to ensure accurate inventory tracking and financial performance review.\nThank you for your continued attention to these processes.\n")
    print("-----------------------------------------------------")
    manager_main(role_id, user_id)

def manager_main(role_id, user_id):
    from Main import main_menu
    clear_screen()
    print("===== Welcome to MANAGER MENU =====")
    print("a. System Administration")
    print("b. Order Management")
    print("c. Financial Management")
    print("d. Inventory Control")
    print("e. Customer Feedback")
    print("f. Account Management")
    print("g. Log Out")

    choice = input("Enter your choice to continue: ").lower()

    if choice == "a":
        system_administration(role_id, user_id)
        pass
    elif choice == "b":
        display_order_list(role_id, user_id)
        pass
    elif choice == "c":
        generate_z_report(role_id, user_id)
    elif choice == "d":
        inventory_control(role_id, user_id)       
    elif choice == "e":
        display_feedbak_list(role_id, user_id)
    elif choice == "f":
        account_management(role_id, user_id)
    elif choice == 'g':
        print("Log out successful. Thank you.")
        return main_menu()
    else:
        print("Invalid option.")
        return manager_main(role_id, user_id)