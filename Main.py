# 1. Must sign in as manager to complete stock initialization as part of the store opening flow
# 2. Must sign in as cashier for item sales report before the manager generates the financial report

def clear_screen():
    """Clears the console screen by printing empty lines."""
    for _ in range(3):
        print("\n")

def main_menu():
    """Displays the main menu and handles user selection."""
    clear_screen()
    print("------- Welcome to KL Baguette Bakery -------")
    print("1. Sign In")
    print("2. Sign Up")
    print("3. Exit")

    choice = input("Select an option: ")

    if choice == '1':
        sign_in()
    elif choice == '2':
        sign_up()
    elif choice == '3':
        print("Thank you. Please visit us again.")
        return
    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        main_menu()  

def sign_up():
    """Handles user sign-up process."""
    print("\nCreate Your Account")

    firstname = input("First Name: ")
    lastname = input("Last Name: ")
    email = input("Email: ")

    if "@gmail.com" in email:
        if check_existing_user(email):  # Check if the email already exists
            print("Email already exists.")
            return sign_in()

        password = input("Password: ")
        if len(password) < 8:
            print("Password is too short. Must be at least 8 characters.")
            sign_up()
            return

        confpassword = input("Confirm your password: ")
        if password != confpassword:
            print("Passwords do not match. Please try again.")
            sign_up()
            return

        role, role_id = role_selection(firstname)  # Capture both role name and role_id
        if role is None:
            print("Role selection failed. Please try again.")
            sign_up()
            return

        # Check if the role_id already exists in user_data.txt
        if existing_role_id(role_id):
            print(f"Role ID '{role_id}' is already assigned to another user. Please sign in.")
            main_menu()  
            return

        new_user_id = generate_user_id()  # Generate the new user ID

        save_user_data(email, password, firstname, lastname, role, role_id, new_user_id)

        print(f"Sign up successful! Your user ID is {new_user_id}. Please sign in to access your account.")
        sign_in()  

    else:
        print("Invalid email. Please use a valid gmail address.")
        sign_up()

def existing_role_id(role_id):
    """Checks if the role_id already exists in user_data.txt."""
    try:
        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) > 0 and data[5] == role_id:  # Compare role_id with data[5] in user_data.txt
                    return True
    except FileNotFoundError:
        return False  # File does not exist yet, so role_id cannot exist
    return False 

def save_user_data(email, password, firstname, lastname, role, role_id, user_id):
    """Saves the user data to user_data.txt."""
    with open("user_data.txt", "a") as file:
        if role == "customer":
            file.write(f"{email},{password},{firstname},{lastname},{role},0,{user_id}\n")
        else:
            file.write(f"{email},{password},{firstname},{lastname},{role},{role_id},{user_id}\n")

def generate_user_id():
    """Generates a unique user ID based on the last entry in user_data.txt."""
    try:
        with open("user_data.txt", "r") as file:
            lines = file.readlines()
            if lines:
                last_user_id = lines[-1].strip().split(",")[-1]  # Get the user ID which is the last element
                if last_user_id:  # Check if last_user_id is not empty
                    increment = int(last_user_id[1:]) + 1
                else:
                    increment = 1  # If last_user_id is empty, start from 1
            else:
                increment = 1  # No users yet, start from 1
    except FileNotFoundError:
        increment = 1  # File does not exist, start from 1
    except IndexError:
        increment = 1  # In case of malformed data, start from 1

    return f"E{increment:03d}"

def check_existing_user(email):
    """Checks if a user already exists based on email."""
    try:
        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) > 0 and data[0] == email:
                    return True
    except FileNotFoundError:
        return False
    return False

def sign_in():
    """Handles user sign-in process."""
    print("\nSign In")
    email = input("Enter email: ")
    password = input("Enter password: ")

    found = False
    user_data = None

    try:
        with open("user_data.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 7 and email == data[0] and password == data[1]:
                    found = True
                    user_data = data  # Store the user's data for later use
                    print(f"Welcome back, {data[2]}!")  # data[2] is the firstname
                    break
    except FileNotFoundError:
        print("Error: user_data.txt file not found.")

    if found and user_data:
        # Pass the user_id along with role to mock_up_role
        mock_up_role(user_data[6], user_data[4], user_data[5])  # Redirect to specific role mockup
    else:
        print("Invalid email or password.")
        main_menu()

def role_selection(firstname):
    """Prompts the user to select their role."""
    print("\nRole Selection")
    print("1. Access specific role (Cashier/Baker/Manager)")
    print("2. Continue as Customer")

    choice = input("Select your role: ")

    if choice == '1':
        role_id = input("Enter your role ID: ")  # Capture user input for role_id
        role_name, valid_role_id = access_role(role_id, firstname)  # Verify the role_id
        if valid_role_id is None:
            return None, None  # Return None if role_id is invalid
        return role_name, valid_role_id  # Return the role name and valid role ID
    elif choice == '2':
        return 'customer', None
    else:
        print("Invalid option. Please try again.")
        return role_selection(firstname)

def access_role(role_id, firstname):
    """Accesses the role-based functionalities based on the role ID."""
    user_roles = {}
    try:
        with open("user_roles.txt", "r") as file:
            for line in file:
                role_id_temp, role_name = line.strip().split(",")
                user_roles[role_id_temp] = role_name
    except FileNotFoundError:
        print("Error: user_roles.txt file not found.")
        return None, None  # Return None in case of file not found

    if role_id in user_roles:
        return user_roles[role_id], role_id  # Return role_name and the exact role_id input
    else:
        print("Invalid role ID.")
        return None, None  # Return None if invalid role_id is entered

def mock_up_role(user_id, role, role_id):
    """Directs the user to the appropriate role-based mockup."""
    if role.lower() == "manager":
        manager_mockup(role_id, user_id)
    elif role.lower() == "cashier":
        cashier_mockup(role_id, user_id)
    elif role.lower() == "baker":
        baker_mockup(role_id, user_id)
    elif role.lower() == "customer":
        customer_mockup(user_id)
    else:
        print("Error: Invalid role.")
        main_menu()

def manager_mockup(role_id, user_id):
    """Access to manager functionalities."""
    from Manager import manager_notice
    manager_notice (role_id, user_id)

def cashier_mockup(role_id, user_id):
    """Access to cashier functionalities."""
    from Cashier import cashier_notice  # Ensure Cashier is imported only where needed
    cashier_notice(role_id, user_id)  # Pass the role_id to cashier functionalities

def baker_mockup(role_id, user_id):
    """Access to baker functionalities."""
    from Bakers import baker_main
    baker_main(role_id, user_id)

def customer_mockup(user_id):
    """Access to customer functionalities."""
    from Customer import customer_main  # Ensure Customer is imported only where needed
    customer_main(user_id)  # Pass the user_id to customer functionalities

if __name__ == "__main__": 
    main_menu()