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

def quantity_selection(item, price_to_use, product_id, cart, user_id, available_stock):
    while True:
        quantity_input = input(f"How many {item}s would you like to add? ").strip()  # Strip whitespace
        if quantity_input.isdigit():  # Ensure input is a valid number
            quantity = int(quantity_input)  # Convert input to int
            if quantity > 0:
                if quantity > available_stock:  # Check if requested quantity exceeds available stock
                    print(f"Not enough stock available. You can only add {available_stock} {item}(s) to your cart.")
                    quantity = available_stock  # Limit to available stock
                total_price = price_to_use * quantity
                cart.append((product_id, item, price_to_use, quantity, total_price, user_id))
                save_to_cart(product_id, item, price_to_use, quantity, total_price, user_id)  # Save to cart
                
                # Print confirmation message
                print(f"\n{quantity} x {item} added to your cart for RM{total_price:.2f}.")
                return  
            else:
                print("Error. Quantity must be a positive number.")
        else:
            print("Error. Please enter a valid number.")  # Handling invalid input

def user_selection(menu, cart, user_id):
    display_cart(user_id)

    while True:
        selected_product_id = input("\nEnter the product_id to add to your cart (or 0 to cancel): ")
        
        # Check for cancellation
        if selected_product_id == '0':
            print("Cancelled. Returning to the menu.")
            return  # Exit the user selection loop

        found_product = False  # Flag to track if product was found

        for category, products in menu.items():
            for product in products:
                product_id, item, price, discount, discount_price, item_stock = product
                
                if selected_product_id == product_id:
                    found_product = True  # Set flag to true if product is found

                    if item_stock > 0:
                        # Display the selected product details
                        if discount > 0:
                            print(f"You selected: {item} (ID: {product_id}) - Price: RM{discount_price:.2f}")
                            price_to_use = discount_price
                        else:
                            print(f"You selected: {item} (ID: {product_id}) - Price: RM{price:.2f}")
                            price_to_use = price

                        # Call the quantity_selection function to handle quantity input
                        quantity_selection(item, price_to_use, product_id, cart, user_id, item_stock)

                        # Ask if the user wants to add more products
                        add_more = input("Would you like to add more products? (yes/no): ").strip().lower()
                        if add_more != "yes":
                            return  # Exit the user selection loop
                    else:
                        print(f"Sorry, {item} is unavailable.")
                        return  # Exit if the product is unavailable

        if not found_product:
            print("Invalid product ID. Please try again.")  # Message for invalid product ID

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

def save_to_cart(product_id, selected_item, price, quantity, total_price, user_id):
    cart_id = f"CART_{user_id}"
    item_exists = False
    
    try:
        with open("cart.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []  

    new_cart = []
    
    # Check if item already exists in the user's cart
    for line in lines:
        data = line.strip().split(",")
        if data[0] == cart_id:
            # Update the existing item if it's already in the cart
            if data[1] == product_id:
                current_quantity = int(data[3]) + quantity
                total_price = current_quantity * price
                new_cart.append(f"{cart_id},{product_id},{selected_item},{current_quantity},{total_price:.2f},{user_id}\n")
                item_exists = True
            else:
                new_cart.append(line)  

    if not item_exists:
        new_cart.append(f"{cart_id},{product_id},{selected_item},{quantity},{total_price:.2f},{user_id}\n")

    with open("cart.txt", "w") as file:
        file.writelines(new_cart)

    print(f"Saved to cart: {selected_item} (ID: {product_id}) - {quantity} x RM{price:.2f} = RM{total_price:.2f}")

def display_cart(user_id):
    try:
        with open("cart.txt", "r") as file:
            cart_data = file.readlines()
    except FileNotFoundError:
        print("Cart not found in file.")
        return

    user_cart = [line.strip().split(",") for line in cart_data if line.startswith(f"CART_{user_id}")]
    
    if not user_cart:
        print("Your cart is empty.")
        return

    print("Your Cart:")
    index = 1  # Initialize a counter for item numbering
    grand_total = 0.0  # Initialize grand total

    for item in user_cart:
        cart_id, product_id, item_name, quantity, total_price, user_id = item
        
        # Ensure correct types for quantity and total_price
        quantity = int(quantity)  # Convert quantity to int
        total_price = float(total_price)  # Convert total_price to float
        
        grand_total += total_price

        print(f"{index}. {item_name} (ID: {product_id}) - RM{total_price:.2f} x {quantity}")
        index += 1  # Increment the counter

    print(f"Grand Total: RM{grand_total:.2f}")

def remove_from_cart(cart, menu, user_id):
    try:
        with open("cart.txt", "r") as file:
            cart_data = file.readlines()
    except FileNotFoundError:
        print("Your cart is empty. Nothing to remove.")
        return

    if not cart:
        print("Your cart is empty. Cannot removed item.")
        return

    display_cart(user_id)

    delete_product_id = input("Enter the product ID of the item you want to remove (or 0 to cancel): ").strip()
    if delete_product_id == '0':
        return

    found = False
    new_cart = []  
    for line in cart_data:
        data = line.strip().split(",")

        if len(data) < 6:
            print("Invalid cart data. Please check the cart.txt file.")
            return

        cart_id, product_id, item, quantity, total_price, cart_user_id = data
        quantity = int(quantity)  # Convert quantity to integer
        total_price = float(total_price)  # Convert total price to float

        # Check if the product ID matches the one to be removed and belongs to the current user
        if delete_product_id == product_id and cart_user_id == user_id:
            found = True
            print(f"Current quantity of {item}: {quantity}")
            remove_quantity = int(input(f"Enter the quantity to remove from {item} (0 to cancel): ").strip())

            if remove_quantity == 0:
                print("No quantity entered. No items were removed.")
                return
            elif remove_quantity > quantity:
                print(f"Cannot remove {remove_quantity}. You only have {quantity} in your cart.")
                return
            elif remove_quantity == quantity:
                # If removing all, skip adding this item back to the new_cart list
                print(f"{item} has been completely removed from your cart.")
            else:
                # Update the quantity and total price for the item
                new_quantity = quantity - remove_quantity
                price_per_item = total_price / quantity
                new_total_price = new_quantity * price_per_item
                new_cart.append(f"{cart_id},{product_id},{item},{new_quantity},{new_total_price:.2f},{cart_user_id}\n")
                print(f"{remove_quantity} {item}(s) removed. {new_quantity} left.")
        else:
            # Keep the unchanged items in the new cart list
            new_cart.append(line)

    if found:
        with open("cart.txt", "w") as file:
            file.writelines(new_cart)
        print("Cart updated in cart.txt.")
        
        display_cart(user_id)  
    else:
        print("Item not found in your cart.")

def max_custom(current_item_stock, minimum_stock):
    if current_item_stock > minimum_stock:
        return current_item_stock
    else:
        return minimum_stock

def update_item_stock(cart):
    updated_lines = []
    found = False

    with open("product_menu.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 7:
                product_id_in_file = data[1]
                for cart_item in cart:
                    if len(cart_item) != 6:
                        continue  # Skip invalid cart items
                    cart_id, product_id, item_name, quantity, total_price, user_id = cart_item
                    if product_id_in_file == product_id:
                        found = True
                        current_item_stock = int(data[6]) - int(quantity)
                        new_stock = max_custom(current_item_stock, 0)
                        data[6] = str(new_stock)
                        updated_lines.append(f"{','.join(data)}\n")
                        break
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

    if found:
        with open("product_menu.txt", "w") as file:
            file.writelines(updated_lines)

def check_item_validation(cart, menu):
    for cart_item in cart:
        cart_id, product_id, product_name, quantity, total_price, user_id = cart_item
        quantity = int(quantity)

        for category, products in menu.items():
            for product in products:
                prod_id, item, price, discount, discount_price, item_stock = product
                
                if prod_id == product_id:
                    if item_stock >= quantity:
                        continue  # Stock is sufficient, proceed with the next item
                    else:
                        print(f"Item {product_id} - {product_name} is unavailable now.")
                        return False  
    return True  

import datetime

def checkout(user_id, menu):
    try:
        with open("cart.txt", "r") as file:
            cart_data = file.readlines()
    except FileNotFoundError:
        print("Your cart is empty. Cannot proceed to checkout.")
        return

    # Filter cart data for the current user
    cart = [line.strip().split(",") for line in cart_data if line.startswith(f"CART_{user_id}")]

    if not cart:
        print("Your cart is empty. Cannot proceed to checkout.")
        return
    
    if not check_item_validation(cart, menu):
        print("Cannot proceed to checkout due to insufficient stock.")
        return
    # Display cart before payment
    display_cart(user_id)
    print("Pending payment...")

    print("1. E-wallet")
    print("2. Credit/Debit card payment")
    choice = input("Please select your preferred payment method (1 or 2): ")

    if choice == "1":
        payment_method = "e-wallet"
    elif choice == "2":
        payment_method = "Credit/Debit card"
    else:
        print("Invalid payment method.")
        return

    status = "Processing" 
    order_id = generate_order_id()

    # Capture current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("orders.txt", "a") as file:
        for cart_item in cart:
            if len(cart_item) == 6:
                cart_id, product_id, item_name, quantity, total_price, _ = cart_item
                total_price = float(total_price)
                file.write(f"{order_id},{cart_id},{product_id},{item_name},{quantity},{total_price:.2f},{user_id},{status},{payment_method},{current_datetime}\n")

    update_item_stock(cart)
    clear_cart(cart, user_id)
    generate_receipt(order_id)
    ask_for_feedback(user_id, order_id)

def generate_order_id():
    try:
        with open("orders.txt", "r") as file:
            lines = file.readlines()
            if lines:
                for line in reversed(lines):
                    if line.strip():
                        last_order_id = line.strip().split(",")[0]
                        if last_order_id.startswith("ORD"):
                            increment = int(last_order_id[3:]) + 1
                            break
                else:
                    increment = 1
            else:
                increment = 1
    except FileNotFoundError:
        increment = 1

    return f"ORD{increment:03d}"

def clear_cart(cart, user_id):
    cart_id = f"CART_{user_id}"
    with open("cart.txt", "r") as file:
        lines = file.readlines()

    with open("cart.txt", "w") as file:
        for line in lines:
            if not line.startswith(cart_id):
                file.write(line)

    cart.clear()

def generate_receipt(order_id):
    try:
        with open("orders.txt", "r") as file:
            lines = file.readlines()
            order_details = []
            for line in lines:
                if line.startswith(order_id):
                    details = line.strip().split(",")
                    if len(details) == 10:  
                        order_details.append(details)

        if order_details:
            print("----------------------------------------")
            print(f"Receipt for Order ID: {order_id}")
            print("----------------------------------------")
            print(f"{'Qty':<5} {'Item ID':<10} {'Item Name':<30} {'Price (RM)':<10}")
            total_amount = 0
            for details in order_details:
                product_id = details[2]
                quantity = int(details[4])
                total_price = float(details[5])
                payment_method = details[8]
                order_datetime = details[9]

                with open("product_menu.txt", "r") as menu_file:
                    menu_lines = menu_file.readlines()
                    for menu_line in menu_lines:
                        menu_details = menu_line.strip().split(",")
                        if len(menu_details) >= 7 and menu_details[1] == product_id:
                            item_name = menu_details[2]
                            break
                    else:
                        item_name = "Unknown Item"

                print(f"{quantity:5}   {product_id:10} {item_name:30} {total_price:6.2f}")
                total_amount += total_price
            print("----------------------------------------")
            print(f"Total Amount: RM{total_amount:.2f}")
            print(f"Payment Method: {payment_method}")
            print(f"Order Date and Time: {order_datetime}")
            print("----------------------------------------")

        else:
            print("Order not found.")
    
    except FileNotFoundError:
        print("No orders found.")

def update_order_status():
    found = False
    update_lines = []
    
    with open("orders.txt", "r") as file:
        lines = file.readlines()
    
    for line in lines:
        order_line = line.strip()
        data = order_line.split(",")
        
        if len(data) >= 10:
            data[7] = "Completed"  
            found = True

        updated_line = ",".join(data) + "\n"
        update_lines.append(updated_line)
    
    if found:
        with open("orders.txt", "w") as file:
            file.writelines(update_lines)
        print("Order status updated to 'Completed'.")
    else:
        print("No orders were found to update.")

def check_order_status(user_id):
    try:
        with open("orders.txt", "r") as file:
            orders = {}
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 9:  
                    order_id = data[0]
                    cart_id = data[1]
                    product_id = data[2]
                    item_name = data[3]
                    quantity = int(data[4])
                    total_price = float(data[5])  
                    user_id_in_file = data[6]
                    order_status = data[7]
                    payment_method = data[8]
                    order_datetime_str = data[9]

                    if order_id not in orders:
                        orders[order_id] = {
                            'user_id': user_id_in_file,
                            'items': [],
                            'status': order_status,
                            'payment_method': payment_method,
                            'order_datetime': order_datetime_str
                        }

                    orders[order_id]['items'].append((product_id, item_name, quantity, total_price))

        found = False
        latest_order_id = None
        latest_order_datetime = None
        for order_id, details in orders.items():
            if details['user_id'] == user_id:
                if latest_order_datetime is None or details['order_datetime'] > latest_order_datetime:
                    latest_order_id = order_id
                    latest_order_datetime = details['order_datetime']
                print(f"\nOrder ID: {order_id}")
                print("--------------------------------------------------------")
                print(f"{'ID':<5} {'Item Name':<25} {'Qty':<10} {'Total Price':<10}")
                print("--------------------------------------------------------")
                for product_id, item_name, quantity, total_price in details['items']:
                    print(f"{product_id:<5} {item_name:<25} {quantity:<10} RM{total_price:.2f}")
                print("--------------------------------------------------------")
                print(f"Status: {details['status']}")
                print(f"Payment Method: {details['payment_method']}\n")
                found = True
                
        if not found:
            print("No orders found for this user.")
            return

        if latest_order_id is not None and orders[latest_order_id]['status'] == 'Processing':
            print("Please provide feedback for your latest order.\n")
            ask_for_feedback(user_id, order_id)
            return 

    except FileNotFoundError:
        print("No orders found.")

def ask_for_feedback(user_id, order_id):
    try:
        with open("orders.txt", "r") as file:
            order_data = file.readlines()
    except FileNotFoundError:
        print("No order data found.")
        return

    order_items = [line.strip().split(",") for line in order_data if line.startswith(order_id) and line.split(",")[6] == user_id]

    if not order_items:
        print("No matching order found.")
        return

    for item in order_items:
        product_id = item[2]  
        item_name = item[3] 

        print("Please leave a feedback to complete your order.")
        feedback = input(f"Please provide your feedback for Product '{item_name}' - Product ID {product_id} (0 to cancel): ").strip()
        if feedback == "0":
            print("Your order is not completed without feedback.")
            return
        elif feedback == "":
            feedback_id = generate_feedback_id()
            with open("feedback.txt", "a") as file:
                file.write(f"{feedback_id},{user_id},{order_id},{product_id},None\n")
            print(f"Thank you! Your feedback for '{item_name}' has been saved with Feedback ID: {feedback_id}")
            if feedback != "0":
                update_order_status()
        else:
            feedback_id = generate_feedback_id()
            with open("feedback.txt", "a") as file:
                file.write(f"{feedback_id},{user_id},{order_id},{product_id},{feedback}\n")
            print(f"Thank you! Your feedback for '{item_name}' has been saved with Feedback ID: {feedback_id}")
            if feedback != "0":
                update_order_status()

def generate_feedback_id():
    try:
        with open("feedback.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                last_feedback_id = last_line.split(",")[0]
                feedback_number = int(last_feedback_id[1:]) + 1
            else:
                feedback_number = 1
    except FileNotFoundError:
        feedback_number = 1

    return f"F{feedback_number:03d}"

def account_management(user_id):
    print("-----Manage Your Account-----")
    print("i. Edit First Name")
    print("ii. Edit Last Name")
    print("iii. Change Password")
    choice = input("ENTER A CHOICE: ")
    
    if choice == "i":
        modify_firstname(user_id)
    elif choice == "ii":
        modify_lastname(user_id)
    elif choice == "iii":
        modify_password(user_id)
    else:
        print("Invalid option")
        return 

def modify_firstname(user_id):
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

def modify_lastname(user_id):
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

def modify_password(user_id):
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

def customer_main(user_id):
    from Main import main_menu
    clear_screen()
    cart = []
    menu = product_list()

    try:
        with open("cart.txt", "r") as file:
            cart_data = file.readlines()
            cart = [line.strip().split(",") for line in cart_data if line.startswith(f"CART_{user_id}")]
    except FileNotFoundError:
        print("File not found.")
    
    while True:
        print("----------- KL Baguette Bakery Menu -----------")
        print("\nOptions:")
        print("1. View Menu and Add Items to Cart")
        print("2. View Shopping Cart")
        print("3. Remove Items from Cart")
        print("4. Checkout")
        print("5. Check Orders Status & Feedback")
        print("6. Manage Account")
        print("7. Log Out")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            display_menu(menu)
            user_selection(menu, cart, user_id)
        elif choice == '2':
            display_cart(user_id)  
        elif choice == '3':
            remove_from_cart(cart, menu, user_id)  
        elif choice == '4':
            checkout(user_id, menu)
        elif choice == "5":
            check_order_status(user_id)
        elif choice == '6':
            account_management(user_id)
        elif choice == '7':
            print("Log out successful. Thank you.")
            return main_menu()        
        else:
            print("Invalid choice. Please try again.")