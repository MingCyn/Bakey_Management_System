def clear_screen():
    for _ in range(3):
        print("\n")

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

def display_menu(menu):
    print(f"{'ID':<5} {'Item':<30} {'Price':<10}")
    for category, products in menu.items():
        print(f"\n{category}:")
        for product in products:
            product_id, item, price, discount, discount_price, item_stock = product
            if item_stock > 0:
                if discount > 0:
                    print(f"{product_id:<5} {item:<30} RM{price:<10.2f} Discount:{discount}%  Discount Price:RM{discount_price:.2f}")
                else:
                    print(f"{product_id:<5} {item:<30} RM{price:.2f}")
            else:
                print(f"{product_id:<5} {item:<30} unavailable")

def apply_discount(price, discount):
    if discount > 0:
        return price * (1 - discount / 100)
    return price

def modify_product_list(role_id, user_id):
    menu = product_list()
    display_menu(menu)
    modify_item_id = input("Enter product ID to modify product detail: ")
    updated_lines = []
    found = False
    modified_data = None

    with open("product_menu.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 6 and modify_item_id == data[1]:
                found = True
                print(f"Found product: {data[0]} - {data[1]} - {data[2]} - RM{data[3]} - {data[4]}% - Price after discount: RM{float(data[5]):.2f}\n")
                modified_data = data  
            else:
                updated_lines.append(line)  

    if found:
        modified_data = product_detail(modify_item_id, modified_data)  
        if modified_data:  
            updated_lines.append(f"{modified_data[0]},{modified_data[1]},{modified_data[2]},{modified_data[3]},{modified_data[4]},{modified_data[5]},{modified_data[6]}\n")
        
        with open("product_menu.txt", "w") as file:
            for line in updated_lines:
                if not line.endswith("\n"):  # Add a newline if it's missing
                    line += "\n"
                file.write(line)
        return modify_menu(role_id, user_id)
    else:
        print("Product ID not found.")
        return modify_menu(role_id, user_id)
    
def modify_product_name(data):
    print(f"Current Product Name: {data[2]}")
    new_product_name = input("Enter new product name: ")
    data[2] = new_product_name
    print("Product name updated.")
    return data

def modify_price(data):
    print(f"Current Product Price: RM{data[3]}")
    try:
        new_price = float(input("Enter new product price (without RM): "))
    except ValueError:
        print("Invalid price format. Please enter a valid number.")
        return data 
    
    data[3] = f"{new_price:.2f}"
    print("Product price updated.")
    return data

def modify_item_discount(data):
    print(f"Current Discount: {data[4]}%")
    try:
        new_discount = float(input("Enter discount percentage (do not include %): "))
    except ValueError:
        print("Invalid discount format. Please enter a valid number.")
        return data
    
    data[4] = f"{int(new_discount)}"
    discount_price = apply_discount(float(data[3]), int(new_discount))
    data[5] = f"{discount_price:.2f}"
    print(f"Discount updated. New price after discount: RM{discount_price:.2f}")
    return data

def product_detail(modify_item_id, data):
    while True:
        print(f"\nSelect the option to modify product detail for {modify_item_id}:")
        print("1. Product Name") 
        print("2. Price") 
        print("3. Single Item Discount")
        print("4. Quit from modification")

        choice = input("ENTER A CHOICE: ")
            
        if choice == "1":
            data = modify_product_name(data)
        elif choice == "2":
            data = modify_price(data)
        elif choice == "3":
            data = modify_item_discount(data)
        elif choice == "4":
            print("Exiting modification.")
            break
        else:
            print("Invalid option, please try again.")
    
    return data  # Return the updated data after all modifications

def add_new_product(role_id, user_id):
    menu = {}
    used_alphabets = set()  

    with open("product_menu.txt", "r") as file:
        for line in file:
            category, product_id, item, price, discount, discount_price, item_stock = line.strip().split(",", 7)
            if category not in menu:
                menu[category] = []
            menu[category].append((product_id, item, float(price), discount))
            used_alphabets.add(product_id[0])  # Add the first letter of product_id to used_alphabets

    category_input = input("Enter the category of the new product (e.g., Bread, Pastries, Cakes, Cookies) **'0' to cancel**: ")
    if category_input == '0':
        print("Product addition canceled.")
        return modify_menu(role_id, user_id) 
    
    category = None
    for existing_category in menu.keys():
        if existing_category.lower() == category_input.lower():
            category = existing_category
            break
    
    if category is None:
        category = category_input 

    product_name = input("Enter the name of the new product: ")

    try:
        price = float(input("Enter the price of the new product (without RM): "))
    except ValueError:
        print("Invalid price format. Please enter a valid number.")
        return

    try:
        discount = float(input("Enter discount percentage (do not include %): "))
        if discount < 0:
            print("Discount amount cannot be negative.")
            return
    except ValueError:
        print("Invalid discount format. Please enter a valid number.")
        return

    if category in menu:
        last_product_id = menu[category][-1][0]  
        increment = int(last_product_id[1:]) + 1  
        new_product_id = f"{last_product_id[0]}{increment:02d}"  
    else:
        while True:
            new_category = input("Enter an alphabet for new category ID (e.g., A, B, C): ")
            if new_category in used_alphabets:
                print(f"The alphabet '{new_category}' for product IDs already exists. Please choose another alphabet.")
            else:
                used_alphabets.add(new_category)
                new_product_id = f"{new_category}01"
                menu[category] = []  # Initialize new category in menu
                break

    discount_price = apply_discount(price, discount)

    new_product = f"{category},{new_product_id},{product_name},{price:.2f},{int(discount)},{discount_price:.2f},0\n"

    with open("product_menu.txt", "a") as file:
        file.write(new_product)  

    clear_screen()
    print(f"New product added: {category} - {new_product_id} - {product_name} - RM{price:.2f} - {int(discount)}% - Price after discount: RM{discount_price:.2f}\n")
    return modify_menu(role_id, user_id)

def delete_item(role_id, user_id):
    menu = product_list()
    display_menu(menu)
    delete_item_id = input("Enter product ID to delete: ")
    updated_menu_lines =[]
    updated_ingredient_lines = []
    updated_recipe_lines =[]
    found = False

    with open("product_menu.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 6 and delete_item_id == data[1]:
                found = True
                print(f"Are you sure you would like to delete this item: {data[1]} - {data[2]}")
                delete_product = input("Please enter yes or no: ").lower()
                
                if delete_product == "yes":
                    print("Product deleted successfully.")
                else:
                    print("Deletion cancelled.")
                    updated_menu_lines.append(line) 
            else:
                updated_menu_lines.append(line)   

    with open("ingredient_needed.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 7 and delete_item_id == data[0]:
                continue
            else:
                updated_ingredient_lines.append(line) 
    
    with open ("recipe.txt","r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 4 and delete_item_id == data[1]:
                continue
            else:
                updated_recipe_lines.append(line)

    if found:
        with open("product_menu.txt", "w") as file:
            file.writelines(updated_menu_lines)  
        print("Product Menu updated.")

        with open ("ingredient_needed.txt","w") as file:
            file.writelines(updated_ingredient_lines) 

        with open ("recipe.txt","w") as file:
            file.writelines(updated_recipe_lines) 
    else:
        print("Product ID not found.")
    
    return modify_menu(role_id, user_id)

def modify_menu(role_id, user_id):
    clear_screen()
    print("------Manage Product Menu------")
    print("i. Modify Product Detail")
    print("ii. Add New Item")
    print("iii. Delete Item")
    print("iv. Exit Manage Product Menu")
    choice = input("ENTER A CHOICE: ")

    if choice == "i":
        clear_screen()
        modify_product_list(role_id, user_id)
    elif choice == "ii":
        clear_screen()
        add_new_product(role_id, user_id)
    elif choice == "iii":
        clear_screen()
        delete_item(role_id, user_id)
    else:
        print("Exiting Manage Product Menu...")
        cashier_main(role_id, user_id)

import datetime

def max_custom(current_item_stock, minimum_stock):
    if current_item_stock > minimum_stock:
        return current_item_stock
    else:
        return minimum_stock

def sum_custom(initial_value, current_price):
    total = initial_value
    for price in current_price:
        total += price
    return total

def find_best_sellers_products(product_sales):
    top_5_products = []
    
    while len(top_5_products) < 5:
        max_product = None
        max_quantity = -1  

        for product_id, data in product_sales.items():
            # Skip already added products by checking product_id instead of name
            if product_id in [prod['id'] for prod in top_5_products]:
                continue  # Skip already added products

            if max_custom(data['quantity'], max_quantity) == data['quantity']:
                max_quantity = data['quantity']
                max_product = {'id': product_id, **data}

        if max_product:
            top_5_products.append(max_product)

        if len(top_5_products) == len(product_sales):
            break

    return top_5_products

def generate_sales_report(role_id):
    product_sales = {}
    product_categories = {}  # Initialize the product categories dictionary
    total_items_sold = 0
    total_sales = 0.0

    with open("product_menu.txt", "r") as file:
        for line in file:
            category, product_id, item, price, discount, discount_price, item_stock = line.strip().split(",")
            product_categories[product_id] = (category, item)  # Store category and item name

    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    
    with open("orders.txt", "r") as file:
        for line in file:
            order_id, cart_id, product_id, product_name, quantity, total_price, user_id, status, payment_method, timestamp = line.strip().split(",")
            
            order_date = timestamp.split(" ")[0]
            
            if order_date == current_date:
                quantity = int(quantity)
                total_price = float(total_price)

                total_items_sold += quantity
            
                if product_id not in product_sales:
                    product_sales[product_id] = {'name': product_name,'quantity': 0,'total_price': 0.0}

                # Update product sales information
                product_sales[product_id]['quantity'] += quantity
                product_sales[product_id]['total_price'] += total_price

    top_selling_products = find_best_sellers_products(product_sales)
    # Group sales data by category based on product_categories
    categorised_sales = {}
    for product_id, data in product_sales.items():
        category, item_name = product_categories.get(product_id, (None, None))
        if category is not None:
            if category not in categorised_sales:
                categorised_sales[category] = []
            categorised_sales[category].append((product_id, data))

    total_sales = sum_custom(0, (data['total_price'] for data in product_sales.values())) 
    #sum of all total_price values in the product_sales dictionary and stores the result in total_sales

    current_time = current_datetime.strftime("%H:%M:%S")

    print("--------------------------------------------------------------------")
    print(f"                        Item Sales Report")
    print("--------------------------------------------------------------------")
    print(f"Bakery Name: KL Baguette")
    print(f"Date: {current_date}")
    print(f"Time: {current_time}")
    print(f"Cashier ID: {role_id}")
    print("--------------------------------------------------------------------")
    
    print("Item Sales Overview")
    print("--------------------------------------------------------------------")
    print(f"Total Items Sold: {total_items_sold}")
    print(f"Total Revenue: RM{total_sales:,.2f}")
    print("--------------------------------------------------------------------")
    
    print("Detailed Item Sales Breakdown")
    print("--------------------------------------------------------------------")
    print(f"{'Item ID':<10}{'Item Name':<30}{'Qty Sold':<10}{'Unit Price':<15}{'Total Sales'}")
    
    for category, items in categorised_sales.items():  # Iterate through each category
        for product_id, data in items:
            unit_price = data['total_price'] / data['quantity'] if data['quantity'] > 0 else 0  
            print(f"{product_id:<10}{data['name']:<30}{data['quantity']:<10}RM{unit_price:>5,.2f}{' ':<10}RM{data['total_price']:>5,.2f}")

    print(f"\n{'Total':<40}{total_items_sold:<27}RM{total_sales:,.2f}")
    print("--------------------------------------------------------------------")
    print("Top 5 Best-Selling Products:")
    print("--------------------------------------------------------------------")
    print(f"{'Rank':<5}{'Product Name':<30}{'Units Sold':<12}{'Total Sales':<15}")

    rank = 1
    for product in top_selling_products:
        print(f"{rank:<5}{product['name']:<30}{product['quantity']:<12}RM{product['total_price']:<15,.2f}")
        rank += 1

    print("--------------------------------------------------------------------")

    save_sales_record(role_id, current_datetime, total_items_sold, total_sales)
    return cashier_main(role_id, user_id)

def save_sales_record(role_id, current_datetime, total_items_sold, total_sales):
    new_sales_record = f"{current_datetime},{total_items_sold},{total_sales:.2f},{role_id}\n"
    
    try:
        # Append the new sales record to the file
        with open("sales_record.txt", "a") as file:  # Open in append mode
            file.write(new_sales_record)  # Write the new record
        print(f"{current_datetime} sales report saved.")
    except FileNotFoundError:
        # If the file doesn't exist, create a new one
        with open("sales_record.txt", "w") as file:
            file.write(new_sales_record)
        print(f"{current_datetime} sales report saved.")
    
def print_latest_receipt(role_id, user_id):
    try:
        with open("orders.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_order_id = lines[-1].strip().split(",")[0]
                order_details = []
                for line in lines:
                    order_id, cart_id, product_id, item_name, quantity, total_price, user_id, status, payment_method, current_datetime = line.strip().split(",")
                    if order_id == last_order_id:
                        order_details.append((product_id, item_name, quantity, total_price, payment_method, current_datetime))
                if order_details:
                    print("----------------------------------------")
                    print(f"Receipt for Order ID: {last_order_id}")
                    print("----------------------------------------")
                    print(f'User ID:{user_id}\n')
                    print(f"{'Qty':<5} {'Item ID':<10} {'Item Name':<30} {'Price (RM)':<10}")
                    total_amount = 0
                    for details in order_details:
                        product_id, item_name, quantity, total_price, payment_method, current_datetime = details
                        print(f"{quantity:4}   {product_id:10} {item_name:30} RM{float(total_price):6.2f}")
                        total_amount += float(total_price)
                    print("----------------------------------------")
                    print(f"Total Amount: RM{total_amount:.2f}")
                    print(f"Payment Method: {payment_method}")
                    print(f"Order Date and Time: {current_datetime}")
                    print("----------------------------------------")
                else:
                    print("No orders found.")
            else:
                print("No orders found.")
    
    except FileNotFoundError:
        print("No orders found.")
    return print_receipt_main(role_id, user_id)

def search_specific_user_receipt(role_id, user_id):
    check_user_id = input("Enter user_id to print receipt:")

    with open("orders.txt", "r") as file:
        lines = file.readlines()
        last_order_details = None  
        last_order_datetime = None  

        for line in lines:
            order_id, cart_id, product_id, item_name, quantity, total_price, user, status, payment_method, current_datetime = line.strip().split(",")

            if check_user_id == user and status == "Completed":
                if last_order_datetime is None or current_datetime > last_order_datetime:
                    last_order_details = [(order_id, cart_id, product_id, item_name, quantity, total_price, payment_method, current_datetime)]
                    last_order_datetime = current_datetime  # Update the last order datetime
                elif current_datetime == last_order_datetime:
                    last_order_details.append((order_id, cart_id, product_id, item_name, quantity, total_price, payment_method, current_datetime))
                else:
                    return

        if last_order_details:
            print("----------------------------------------")
            print(f"Receipt")
            print("----------------------------------------")
            print(f'User ID: {check_user_id}\n')
            print(f"{'Qty':<5} {'Item ID':<10} {'Item Name':<30} {'Price (RM)':<10}")
            total_amount = 0
            for order in last_order_details:
                order_id, cart_id, product_id, item_name, quantity, total_price, payment_method, current_datetime = order
                print(f"{quantity:5} {product_id:10} {item_name:30} RM{float(total_price):6.2f}")
                total_amount += float(total_price)
            print("----------------------------------------")
            print(f"Total Amount: RM{total_amount:.2f}")
            print(f"Payment Method: {payment_method}")
            print(f"Order Date and Time: {current_datetime}")
            print("----------------------------------------")
        else:
            print("No completed orders found for the specified user.")
    return print_receipt_main(role_id, user_id)

def print_receipt_main(role_id, user_id):
    clear_screen()
    print("----Manage Receipt----")
    print("i. Print latest receipt")
    print("ii. Search customer receipt & print")
    print("iii. Exits Manage Receipt")
    choice = input ("Select an option:")
    if choice == "i":
        clear_screen()
        print_latest_receipt(role_id, user_id)
    elif choice == "ii":
        clear_screen()
        search_specific_user_receipt(role_id, user_id)
    else:
        print("Exiting Manage Receipt...")
        return cashier_main(role_id, user_id)

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
            cashier_main(role_id, user_id)
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

def cashier_notice(role_id, user_id):
    print("-----------------------------------------------------")
    print("NOTICE: Sales Report for Store Closing\n")
    print("To all cashiers,")
    print("Please ensure that you generate the sales report at the end of your shift before closing the store.\nThis step is essential to ensure accurate daily sales tracking.\n")
    print("Reminder:")
    print("Verify that all transactions for the day are included in the report.")
    print("Your attention to this process is greatly appreciated and critical for smooth operations.")
    print("Thank You.")
    print("-----------------------------------------------------")
    cashier_main(role_id, user_id)

def cashier_main(role_id, user_id):
    from Main import main_menu
    clear_screen()
    print("===== Welcome to CASHIER MENU ====")
    print("a. Manage Product Menu")
    print("b. Sales Report")
    print("c. Generate Receipt")
    print("d. Account Management") 
    print("e. Log Out")
    choice = input("ENTER A CHOICE: ")

    if choice == "a":
        clear_screen()
        modify_menu(role_id, user_id)
    elif choice == "b":
        clear_screen()
        generate_sales_report(role_id)
    elif choice == "c":
        clear_screen()
        print_receipt_main(role_id, user_id)
    elif choice == "d":
        clear_screen()
        account_management(role_id, user_id)
    elif choice == "e":
        clear_screen()
        print("Log out successful. Thank you.")
        return main_menu()  
    else:
        print("Invalid option.")
        return cashier_main(role_id, user_id)