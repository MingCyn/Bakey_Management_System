def clear_screen():
    for _ in range(3):
        print("\n")

def display_ingredient(ingredients, role_id, user_id):
    print(f"{'ID':<10} {'Ingredient Name':<30} {'Net Weight':<15} {'Stock':<8} {'Unit Price':<15}")
    for ingredient_id, (name, net_weight, stock, unit_price, current_weight_left) in ingredients.items():
        print(f"{ingredient_id:<10} {name:<30} {net_weight:<15} {stock:<8} RM{unit_price:.2f}")
    return inventory_check_main(role_id, user_id)

def read_ingredient_list():
    ingredient = {}
    with open("ingredient.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            ingredient_id, name, net_weight, stock, unit_price, current_weight_left = line.strip().split(',', 5)  # Fixed split to 4
            ingredient[ingredient_id] = (name, net_weight, int(stock), float(unit_price), int(current_weight_left))  # Store data directly
    return ingredient

def add_ingredient(role_id, user_id):
    ingredient_name = input("Enter new ingredient name (0 to cancel): ")
    if ingredient_name == '0':
        return inventory_check_main(role_id, user_id)

    ingredient_exists = False
    ingredient_id = None

    with open("ingredient.txt", "r") as file:
        lines = file.readlines()
        
        for line in lines:
            data = line.strip().split(",")
            if ingredient_name.lower() == data[1].lower():  
                ingredient_exists = True
                ingredient_id = data[0]
                print(f"Ingredient exists with ID: {ingredient_id}")
                break

    if not ingredient_exists:
        net_weight = input(f"Enter net weight of the {ingredient_name} per package: ")
        price = input(f"Enter price for 1 package of {ingredient_name}: RM ")

        new_id = f"INGR{len(lines) + 1:03d}"  # Incremental ingredient ID
        new_ingredient = f"{new_id},{ingredient_name},{net_weight},0,{price},0\n"

        with open("ingredient.txt", "a") as file:
            file.write(new_ingredient)  # Append new ingredient data as a new line

        print(f"Added new ingredient: {ingredient_name} with ID: {new_id}")
    
    return inventory_check_main(role_id, user_id)

def remove_ingredient(role_id, user_id):
    delete_ingredient_id = input("Enter ingredient ID to delete: ")
    updated_lines = []
    found = False

    with open("ingredient.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 2 and delete_ingredient_id == data[0]:
                found = True
                print(f"Are you sure you would like to delete this ingredient: {data[0]} - {data[1]}")
                delete_product = input("Please enter yes or no (yes/no): ").lower()

                if delete_product == "yes":
                    print("Ingredient deleted successfully.")
                    continue  # Skip adding this line to updated_lines (deletes the ingredient)
                else:
                    print("Deletion cancelled.")
                    updated_lines.append(line)  # Keep the line 
            else:
                updated_lines.append(line)  
    if found:
        with open("ingredient.txt", "w") as file:
            file.writelines(updated_lines)  
    else:
        print("Ingredient ID not found.")

    inventory_check_main(role_id, user_id) 

def inventory_check_main(role_id, user_id):
    clear_screen()
    print("------Inventory Check------")
    print("a. View Ingredient List")
    print("b. Add new Ingredient")
    print("c. Remove Ingredient")
    print("d. Exit from Inventory Check")
    choice = input("ENTER A CHOICE: ")

    if choice == 'a':
        ingredients = read_ingredient_list() 
        display_ingredient(ingredients, role_id, user_id)
    elif choice == 'b':
        add_ingredient(role_id, user_id)
    elif choice == 'c':
        remove_ingredient(role_id, user_id)
    else:
        print("Exit from Inventory Check...")
        return baker_main(role_id, user_id)
    
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
    print(f"{'ID':<5} {'Item':<30}")
    for category, products in menu.items():
        print(f"\n{category}:")
        for product in products:
            product_id, item, price, discount, discount_price, item_stock = product
            if item_stock > 0:
                if discount > 0:
                    print(f"{product_id:<5} {item:<30}")
                else:
                    print(f"{product_id:<5} {item:<30}")
            else:
                print(f"{product_id:<5} {item:<30}")

def ingredient_needed_list():
    ingredient_needed = {}
    ingredients = {}
    with open("ingredient.txt", "r") as ingredient_file:
        for line in ingredient_file:
            data = line.strip().split(',')
            ingredients[data[0]] = data[1:]

    with open("ingredient_needed.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(',')
            product_id, ingredient_needed_id = data[:2]
            
            ingredients_quantities = []
            for item in data[2:]:
                if 'INGR' in item:
                    ingredient_id, quantity = item.strip().split(':')
                    
                    # Check if the ingredient_id exists in ingredient.txt
                    if ingredient_id not in ingredients:
                        print(f"Ingredient ID '{ingredient_id}' doesn't exist. Couldn't proceed for recipe.")
                        return  # Exit if an ingredient is missing
                    ingredients_quantities.append((ingredient_id, quantity))
                else:
                    break

            details_index = 2 + len(ingredients_quantities)
            yields, prep_time, rest_time, cook_time = data[details_index:]

            ingredient_needed[product_id] = {
                'ingredient_needed_id': ingredient_needed_id,
                'ingredients_quantities': [i.split(':') for i in ingredients_quantities],  # Split each INGR###:quantity
                'yields': yields.strip(),
                'prep_time': prep_time.strip(),
                'rest_time': rest_time.strip(),
                'cook_time': cook_time.strip()
            }
    return ingredient_needed

def recipe_list():
    recipe = {}
    with open("recipe.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(',', 3)  # Split into 4 parts
            recipe_id, product_id, ingredient_needed_id, instruction = data
            
            if product_id not in recipe:
                recipe[product_id] = []
            
            recipe[product_id].append(instruction.strip())  # Store instructions by product_id
    
    return recipe

def display_recipe(product_id, ingredient_needed, ingredients, recipe_instructions, products):
    # Read the product name from products dictionary
    for category, product_list in products.items():
        for product in product_list:
            if product[0] == product_id:
                product_name = product[1]
                break
        else:
            continue
        break
    
    print(f"                   {product_name}")
    print(f"Yields: {ingredient_needed[product_id]['yields']}")
    print(f"Prep time: {ingredient_needed[product_id]['prep_time']}")
    print(f"Rest time: {ingredient_needed[product_id]['rest_time']}")
    print(f"Cook time: {ingredient_needed[product_id]['cook_time']}\n")
    
    print("Ingredient:")
    for ingredient_id, quantity in ingredient_needed[product_id]['ingredients_quantities']:
        if ingredient_id not in ingredients:
            print(f"Ingredient ID '{ingredient_id}' doesn't exist. Couldn't proceed for recipe.")
            return  # Exit the function if any ingredient doesn't exist
        
        name, nwt_weight, stock, unit_price, current_weight_left= ingredients[ingredient_id]
        print(f"{name}: {quantity}")

    print("\nInstructions:")
    instructions = recipe_instructions.get(product_id, [])  # Retrieve instructions for the given product_id
    
    if not instructions:  # Check if instructions exist
        print("No instructions available.")
        return

    step_number = 1
    for step in instructions:
        for ingredient_id in ingredients.keys():
            step = step.replace(ingredient_id, ingredients[ingredient_id][0])  # Replace with ingredient name
        print(f"{step_number}. {step}")
        step_number += 1

def show_recipe():
    ingredients = read_ingredient_list()  # Read ingredients
    ingredient_needed = ingredient_needed_list()
    recipe = recipe_list()
    products = product_list()  # Get the product list

    product_id = input("Enter the product ID you would like to see the recipe for (e.g., B01): ")
    if product_id in ingredient_needed:
        display_recipe(product_id, ingredient_needed, ingredients, recipe, products)
    else:
        print("Product ID not found.")
    return manage_recipe_main()

def add_new_recipe():
    add_new_item_id = input("Enter product ID to add recipe: ").upper()
    found = False

    with open("product_menu.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 6 and add_new_item_id == data[1]:
                product_name = data[2]
                product_id = data[1]
                found = True
                print(f"Found product: {data[1]} - {data[2]}")
                break

    if not found:
        print("Product ID not found in product menu. Please ask the Cashier to add the new product before creating the recipe.")
        return

    # Check if recipe already exists
    recipe_exists = False
    with open("recipe.txt", "r") as file:
        for line in file:
            recipe_data = line.strip().split(",")
            if recipe_data and recipe_data[1] == product_id:  
                recipe_exists = True
                print(f"Recipe already exists for {product_name}.")
                return

    ingredients, yields, prep_time, rest_time, cook_time = add_ingredient_needed(product_id, product_name)

    if ingredients is None:
        print("Ingredient collection was not completed due to missing ingredients.")
        return

    save_ingredient_needed_to_file(product_id, ingredients, yields, prep_time, rest_time, cook_time)
    add_recipe_instructions(product_id, ingredients, add_new_item_id)
    print("Recipe and ingredient list added successfully.")

def add_ingredient_needed(product_id, product_name):
    ingredients = []  # List to hold ingredient data in the specified format

    while True:
        ingr_needed_name = input("Enter ingredient (or 'no' to finish): ").strip()  

        if ingr_needed_name.lower() == 'no':
            break  
        
        ingredient_id = check_existing_ingredient(ingr_needed_name)
        
        if ingredient_id:
            print(f"Added ingredient: {ingredient_id} - {ingr_needed_name}")
        else:
            print(f"Ingredient {ingr_needed_name} does not exist. Please add the ingredient before creating a recipe.")
            continue  # retun 

        ingredient_quantity = input(f"Enter quantity needed for {ingr_needed_name} (e.g., 300.0ml): ")
        numeric_value, unit = extract_numeric_value_and_unit(ingredient_quantity)
        if numeric_value <= 0:
            print("Quantity must be greater than 0.")
            continue

        ingredients.append(f"{ingredient_id}:{numeric_value}{unit}")

    if ingredients:  
        yields = input("Enter yield (e.g., 24 cookies): ").strip()
        prep_time = input("Enter preparation time (e.g., 20 minutes): ").strip()
        rest_time = input("Enter rest time (e.g., none): ").strip()
        cook_time = input("Enter cook time (e.g., 15-30 minutes): ").strip()
    else:
        yields = prep_time = rest_time = cook_time = None  

    return ingredients, yields, prep_time, rest_time, cook_time  

def check_existing_ingredient(ingredient_name):
    with open("ingredient.txt", "r") as file:
        for line in file:
            ing_data = line.strip().split(",")
            ingredient_id = ing_data[0]
            existing_name = ing_data[1].lower()  
            
            if existing_name == ingredient_name.lower():
                return ingredient_id  

    return None  

def save_ingredient_needed_to_file(product_id, ingredients, yields, prep_time, rest_time, cook_time):
    ingredient_needed_id = generate_ingredient_needed_id()

    ingredients_string = ','.join(ingredients)

    new_line = f"{product_id},{ingredient_needed_id},{ingredients_string},{yields},{prep_time},{rest_time},{cook_time}\n"

    try:
        with open("ingredient_needed.txt", "r") as file:
            existing_data = file.readlines()
    except FileNotFoundError:
        existing_data = []  

    existing_data.append(new_line)

    with open("ingredient_needed.txt", "w") as file:
        for line in existing_data:
            if not line.endswith("\n"):
                line = line + "\n"
            file.write(line)

    print("Ingredient needed added successfully.\n")

def generate_ingredient_needed_id():
    try:
        with open("ingredient_needed.txt", "r") as file:
            lines = file.readlines()

            for line in reversed(lines):
                if line.strip():  
                    last_ingredient_needed_id = line.strip().split(",")[1].strip()

                    if last_ingredient_needed_id.startswith("D"):
                        increment = int(last_ingredient_needed_id[1:]) + 1  
                        return f"D{increment:03d}"  
            return "D001"

    except FileNotFoundError:
        return "D001"

def get_ingredient_names():
    """Reads ingredient.txt and creates a mapping of ingredient_id to ingredient_name."""
    ingr_dict = {}
    try:
        with open("ingredient.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 2:  # Ensure there's at least ingredient_id and name
                    ingredient_id = data[0]
                    ingredient_name = data[1]
                    ingr_dict[ingredient_id] = ingredient_name
    except FileNotFoundError:
        print("Error: ingredient.txt file not found.")
    return ingr_dict

def ingredient_needed_list():
    ingredient_needed = {}
    with open("ingredient_needed.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(',')
            product_id, ingredient_needed_id = data[:2]
            
            ingredients_quantities = []
            for item in data[2:]:
                if 'INGR' in item:
                    ingredients_quantities.append(item.strip())
                else:
                    break

            details_index = 2 + len(ingredients_quantities)
            yields, prep_time, rest_time, cook_time = data[details_index:]

            ingredient_needed[product_id] = {
                'ingredient_needed_id': ingredient_needed_id,
                'ingredients_quantities': [i.split(':') for i in ingredients_quantities], 
                'yields': yields.strip(),
                'prep_time': prep_time.strip(),
                'rest_time': rest_time.strip(),
                'cook_time': cook_time.strip()
            }
    return ingredient_needed

def display_ingredient_needed_only(add_new_item_id):
    """Displays the ingredient details with names if the input product_id matches a product_id in ingredient_needed.txt."""
    ingredient_needed = ingredient_needed_list()  
    ingr_dict = get_ingredient_names()   
    product_found = False  

    with open("ingredient_needed.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 2 and add_new_item_id == data[0]:  
                product_found = True  
                
                print(f"\nIngredient details for Product ID: {add_new_item_id}")
                ingredients_quantities = ingredient_needed[add_new_item_id]['ingredients_quantities']

                for ingredient_id, quantity in ingredients_quantities:
                    # Fetch ingredient name from the ingr_dict dictionary
                    ingredient_name = ingr_dict.get(ingredient_id, "Unknown Ingredient")
                    print(f"{ingredient_id} ({ingredient_name}) - Quantity: {quantity}")

                print(f"Yields: {ingredient_needed[add_new_item_id]['yields']}")
                break  
    
    if not product_found:
        print(f"No details found for Product ID: {add_new_item_id}")

def add_recipe_instructions(product_id, ingredients, add_new_item_id):
    display_ingredient_needed_only(add_new_item_id)
    
    recipe_id = generate_recipe_id()
    print("\n***Notes: Please use the ingredient ID to replace ingredient name while writing the instruction***")

    instructions = []
    print("Enter recipe instructions (press Enter for a new line, type 'done' on a new line to finish):")
    while True:
        instruction = input()
        if instruction.lower() == 'done':  # Stop input when 'done' is entered
            break
        instructions.append(instruction)  

    try:
        with open("recipe.txt", "r") as file:
            existing_data = file.readlines()

        if existing_data and not existing_data[-1].endswith("\n"):
            existing_data[-1] = existing_data[-1] + "\n"

    except FileNotFoundError:
        existing_data = [] 

    # Open ingredient_needed.txt to retrieve the corresponding ingredient_needed_id
    ingredient_needed_id = None
    try:
        with open("ingredient_needed.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 2 and add_new_item_id == data[0]:
                    ingredient_needed_id = data[1].strip()  
                    break
        if not ingredient_needed_id:
            print("Error: No matching ingredient_needed_id found.")
            return
    except FileNotFoundError:
        print("Error: ingredient_needed.txt not found.")
        return

    with open("recipe.txt", "w") as file:
        for line in existing_data:
            file.write(line)

        for instruction in instructions:
            file.write(f"{recipe_id},{product_id},{ingredient_needed_id},{instruction}\n")

    print("Recipe instructions added successfully.")

def generate_recipe_id():
    try:
        with open("recipe.txt", "r") as file:
            lines = file.readlines()

            # Find the last non-empty line with a valid recipe ID
            for line in reversed(lines):
                if line.strip():  
                    last_recipe_id = line.strip().split(",")[0]  
                    
                    if last_recipe_id.startswith("R"):  
                        increment = int(last_recipe_id[1:]) + 1  
                        return f"R{increment:03d}"  

            return "R001"

    except FileNotFoundError:
        return "R001"
    
def update_ingredient_needed_list(modify_item_id, modify_ingredient_id, new_ingredient_id, new_quantity):
    updated_ingredient_needed_lines = []
    ingredient_found = False

    with open("ingredient_needed.txt","r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(',')
            product_id, ingredient_needed_id = data[:2]

            # Check if the product_id matches the one to modify
            if modify_item_id == product_id:
                ingredients_quantities = []
                # Collect the ingredients from the line
                for item in data[2:]:
                    if 'INGR' in item:
                        ingredients_quantities.append(item.strip())
                    else:
                        break

                # Check for the ingredient that needs to be modified
                updated_ingredients = []
                for ingredient in ingredients_quantities:
                    ingr_id, ingr_amount = ingredient.split(":")
                    if ingr_id.strip() == modify_ingredient_id:
                        # Replace the old ingredient with the new one
                        updated_ingredients.append(f"{new_ingredient_id}: {new_quantity}")
                        ingredient_found = True
                    else:
                        updated_ingredients.append(ingredient)  # Keep other ingredients unchanged

                # Add the unchanged details (yields, prep_time, rest_time, cook_time)
                details_index = 2 + len(ingredients_quantities)
                yields, prep_time, rest_time, cook_time = data[details_index:]
                updated_line = data[:2] + updated_ingredients + [yields, prep_time, rest_time, cook_time]
                updated_ingredient_needed_lines.append(",".join(updated_line) + "\n")
            else:
                # If product_id doesn't match, keep the line unchanged
                updated_ingredient_needed_lines.append(line)

    # If the ingredient was found and replaced, rewrite the file
    if ingredient_found:
        with open("ingredient_needed.txt", "w") as file:
            file.writelines(updated_ingredient_needed_lines)
        
    else:
        print(f"Ingredient {modify_ingredient_id} not found for product {modify_item_id}.")

def replace_ingredient():
    modify_item_id = input("Enter product ID to modify product detail: ").upper()
    updated_recipe_lines = []
    found = False

    with open("product_menu.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 6 and modify_item_id == data[1]:
                product_name = data[2]
                product_id = data[1]
                found = True
                print(f"Found product: {data[1]} - {data[2]}")
                break

    if found:
        recipe_found = False
        with open("ingredient_needed.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(",")
                if len(data) >= 7 and modify_item_id == data[0]:
                    recipe_found = True
                    ingredients_quantities = []
                    for item in data[2:]:
                        if 'INGR' in item:
                            ingredients_quantities.append(item.strip())
                        else:
                            break
                    print("Current ingredients:")
                    ingredient_dict = {}
                    with open("ingredient.txt", "r") as ing_file:
                        for ing_line in ing_file:
                            ing_data = ing_line.strip().split(",")
                            if len(ing_data) >= 6:
                                ingredient_dict[ing_data[0]] = ing_data[1]
                    for ingredient in ingredients_quantities:
                        ingredient_id = ingredient.split(":")[0]
                        if ingredient_id in ingredient_dict:
                            print(f"{ingredient_id} - {ingredient_dict[ingredient_id]}: {ingredient.split(':')[1]}")
                        else:
                            print(f"{ingredient_id} does not exist in ingredient.txt.")
                            return  # Stop if any ingredient is missing

        if not recipe_found:
            print("Recipe not exists, please add recipe before modify.")
            return

        ingredient_id_to_replace = input("Enter the ingredient ID to replace (e.g., INGR001): ").upper()
        ingredient_id_to_replace_exists = False

        with open("ingredient_needed.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(",")
                if len(data) >= 7 and modify_item_id == data[0] and any(ingredient_id_to_replace in item for item in data[2:]):
                    ingredient_id_to_replace_exists = True

        if not ingredient_id_to_replace_exists:
            print(f"Ingredient {ingredient_id_to_replace} does not exist in ingredient needed list for product_id {modify_item_id}.")
            return

        new_ingredient_id = input("Enter the new ingredient ID to replace with (e.g., INGR005): ").upper()

        with open("ingredient.txt", "r") as ing_file:
            ingredient_found = False
            for line in ing_file:
                data = line.strip().split(",")
                if len(data) >= 6 and new_ingredient_id == data[0].upper():
                    ingredient_found = True
                    new_ingredient_name = data[1]
                    break

        if not ingredient_found:
            print(f"{new_ingredient_id} does not exist. Please add the ingredient in ingredient.txt")
            return

        print(f"You are replacing with: {new_ingredient_id} - {new_ingredient_name}")
        quantity_needed = input(f"Enter the quantity needed for the ingredient in {product_name}: ")

        update_ingredient_needed_list(modify_item_id, ingredient_id_to_replace, new_ingredient_id, quantity_needed)

        with open("recipe.txt", "r") as file:
            recipe_lines = file.readlines()
            for line in recipe_lines:
                if modify_item_id in line and ingredient_id_to_replace in line:
                    updated_line = line.replace(ingredient_id_to_replace, new_ingredient_id)
                    updated_recipe_lines.append(updated_line)
                else:
                    updated_recipe_lines.append(line)

        with open("recipe.txt", "w") as file:
            file.writelines(updated_recipe_lines)

        print(f"Ingredient {ingredient_id_to_replace} replaced with {new_ingredient_id} in {product_name}")
    else:
        print("Product ID not found.")
    return manage_recipe_main()
                  
def manage_recipe_main():
    clear_screen()
    print("------Manage Recipe------")
    print("a. Check Recipe")
    print("b. Modify recipe")
    print("c. Add recipe to New Product")
    choice = input("ENTER A CHOICE (0 to exit): ")

    if choice == 'a':
        show_recipe()
    elif choice == 'b':
        replace_ingredient()
    elif choice == 'c':
        add_new_recipe()
    else:
        print("Quit from Manage Recipe")

def is_numeric(value):
    try:
        float(value)  
        return True
    except ValueError:
        return False

def extract_numeric_value_and_unit(quantity):
    """Extracts the numeric value and unit from a quantity string, with unit conversion as needed."""
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

    # Convert numeric_value to float if it has a value, otherwise default to 0.0
    numeric_value = float(numeric_value) if numeric_value else 0.0
    unit = unit.strip()  # Clean up any surrounding spaces

    # Convert units if necessary
    numeric_value, unit = convert_units(numeric_value, unit)

    return numeric_value, unit

def convert_units(quantity, unit):
    """Converts units for calculations while preserving the original unit for display."""
    if unit == "tsp":
        quantity_in_ml = quantity * 5
        return quantity_in_ml, "ml"  
    
    return quantity, unit

import datetime
from datetime import datetime, timedelta

def update_ingredient_file(updated_ingredients):
    try:
        with open("ingredient.txt", "r") as file:
            lines = file.readlines()

        with open("ingredient.txt", "w") as file:
            for line in lines:
                ingredient_data = line.strip().split(",")
                
                ingredient_id = ingredient_data[0]

                if ingredient_id in updated_ingredients:
                    new_current_weight_left, new_stock_left = updated_ingredients[ingredient_id]
                    
                    ingredient_data[5] = f"{int(new_current_weight_left)}"  
                    ingredient_data[3] = str(int(new_stock_left))  
                    
                    # Join the modified data back into a string
                    updated_line = ",".join(ingredient_data) + "\n"
                else:
                    updated_line = line
                
                file.write(updated_line)
    
    except Exception as e:
        print(f"Error updating ingredient.txt: {str(e)}")

def update_item_stock(product_id, total_quantity):
    updated_lines = []
    found = False

    with open('product_menu.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        category, pid, item, price, discount, discount_price, item_stock = line.strip().split(',')

        if pid == product_id:
            current_stock = int(item_stock)
            new_stock = current_stock + total_quantity  
            updated_lines.append(f"{category},{pid},{item},{price},{discount},{discount_price},{int(new_stock)}\n")
            found = True
        else:
            updated_lines.append(line)

    if found:
        with open('product_menu.txt', 'w') as file:
            file.writelines(updated_lines)
        print(f"\nStock for {product_id} updated successfully to {int(new_stock)}.")
    else:
        print(f"Product ID {product_id} not found in product_menu.txt.")

def write_production_record():
    menu = product_list()
    display_menu(menu)
    item_id_to_produce = input("Enter the product ID to produce: ").strip()
    product_menu = product_list() 
    
    product_found = False
    product_name = ""
    for category in product_menu:
        for product in product_menu[category]:
            if product[0] == item_id_to_produce:  
                product_name = product[1]  
                product_found = True
                break
        if product_found:
            break

    if not product_found:
        print(f"Product ID {item_id_to_produce} not found in product menu.\n")
        return

    print(f"Product Selected: ({item_id_to_produce} - {product_name})")

    ingredient_needed = ingredient_needed_list()  
    recipe_ingredients = ingredient_needed.get(item_id_to_produce, {})

    if not recipe_ingredients:
        print(f"No ingredients found for product ID {item_id_to_produce}.")
        return

    basic_yield_str = recipe_ingredients.get('yields', None) # Ensure 'yields' key exists
    if basic_yield_str:
        numeric_yield, yield_unit = extract_numeric_value_and_unit(basic_yield_str)
        print(f"Basic yield serving: {int(numeric_yield)} {yield_unit}")
    else:
        print(f"No yield information available for product ID {item_id_to_produce}.")
        return

    try:
        multiplier = int(input(f"Enter the total quantity of {product_name} to produce: ").strip())
        total_quantity = numeric_yield * multiplier
    except ValueError:
        print("Error: Please enter a valid number for the quantity.")
        return

    # Find a baker ID in user data
    role_id = ""
    found_baker = False
    with open("user_data.txt", "r") as file:
        for line in file:
            email, password, firstname, lastname, role, role_id, user_id = line.strip().split(",")
            if role.strip().lower() == "baker":
                role_id = role_id
                found_baker = True
                break

    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_time = current_datetime.strftime("%H:%M")

    production_id = generate_production_id()
    
    print("-------------------------------------------------")
    print("                 Production Record")
    print("-------------------------------------------------")
    print(f"Date: {current_date}")
    print(f"Time: {current_time}")
    print(f"Batch Number: {production_id}")
    
    if found_baker:
        print(f"Baker ID: {role_id}")
    else:
        print("No Baker found.")
    
    print(f"Product Name: {product_name}")
    print(f"Quantity produced: {int(total_quantity)} {yield_unit}")
    print(f"\nIngredients required for {int(total_quantity)} {product_name}:")

    ingredient_data = read_ingredient_list() 
    
    sufficient_stock = True
    updated_ingredients = {}

    # Check stock availability for each ingredient
    for ingredient_id, quantity_str in recipe_ingredients['ingredients_quantities']:
        if ingredient_id in ingredient_data:
            ingredient_name, net_weight_str, stock, unit_price, current_weight_left_str = ingredient_data[ingredient_id]
            
            # Convert values to numeric types
            net_weight = float(extract_numeric_value_and_unit(net_weight_str)[0]) # Extract numeric part
            current_weight_left = float(extract_numeric_value_and_unit(current_weight_left_str)[0]) # Extract numeric part
            weight, qty_unit = extract_numeric_value_and_unit(quantity_str)  # Extract numeric value and unit from quantity string
            adjusted_quantity = weight * multiplier 
            
            if adjusted_quantity > current_weight_left:
                print(f"Error: Not enough stock for {ingredient_name}. Needed: {adjusted_quantity:.2f}g, Available: {int(current_weight_left)}g")
                sufficient_stock = False  # Set flag to False if not enough stock
                break 

            new_current_weight_left = current_weight_left - adjusted_quantity
            stock_left = new_current_weight_left // net_weight if net_weight > 0 else 0
            
            # Add the updated values to the dictionary
            updated_ingredients[ingredient_id] = (new_current_weight_left, stock_left)
    
            print(f"{ingredient_name}: {int(adjusted_quantity)}{qty_unit} (Current Weight Left: {int(new_current_weight_left)}g, Stock Left: {int(stock_left)})")

    # If there is sufficient stock, proceed with updates and save production record
    if sufficient_stock:
        for ingredient_id, quantity_str in recipe_ingredients['ingredients_quantities']:
            adjusted_quantity = weight * multiplier  # Adjusted from original context
            update_ingredient_file(updated_ingredients)

        update_item_stock(item_id_to_produce, total_quantity)

        print(f"\nPreparation Time: {recipe_ingredients['prep_time']}")
        print(f"Rest Time: {recipe_ingredients['rest_time']}")
        print(f"Cook Time: {recipe_ingredients['cook_time']}")

        notes = input("Write down the notes here if necessary (or 0 if no notes): ").strip()  
        if notes == '0': 
            notes = "None"

        expiration_date = current_datetime + timedelta(days=3)
        # Save production record to production_record.txt
        save_production_record(item_id_to_produce, product_name, total_quantity, recipe_ingredients, role_id, notes, expiration_date)

        print("Production record successfully saved.")
    else:
        print("Production halted due to insufficient stock. No production record saved.")
    return production_record_keeping(role_id)

def save_production_record(item_id_to_produce, product_name, total_quantity, recipe_ingredients, baker_id, notes, expiration_date):
    production_id = generate_production_id()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expiration_date = expiration_date.strftime("%d/%m/%y")

    notes = notes if notes.strip() else "None"

    with open("production_record.txt", "a") as file:
        file.write(f"{production_id},{current_datetime},{item_id_to_produce},{product_name},{int(total_quantity)},{baker_id},{notes},{expiration_date}\n")

def production_record_list():
    production_record = []
    with open("production_record.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            production_id, current_datetime, item_id_to_produce, product_name, total_quantity, baker_id, notes, expiration_date = line.strip().split(',', 7)
            production_record.append((production_id, current_datetime, item_id_to_produce, product_name, total_quantity, baker_id, notes, expiration_date))  # Append user details as a tuple
    return production_record

def view_production_record_list(production_record,role_id):
    print(f"{'Batch ID':<13} {'Date Time':<20} {'Product ID':<12} {'Product Name':<25} {'Qty Produced':<15} {'Baker ID':<10} {'Notes':<20}{'Expiration date':<15}")
    for record in production_record:
        production_id, current_datetime, item_id_to_produce, product_name, total_quantity, baker_id, notes, expiration_date = record
        print(f"{production_id:<13} {current_datetime:<20} {item_id_to_produce:<12} {product_name:<25} {total_quantity:<15} {baker_id:<10} {notes:<20} {expiration_date:<10}")
    return production_record_keeping(role_id)

def generate_production_id():
    try:
        with open("production_record.txt", "r") as file:
            lines = file.readlines()
            if lines:
                for line in reversed(lines):
                    if line.strip():
                        last_production_id = line.strip().split(",")[0]
                        if last_production_id.startswith("PRD"):
                            increment = int(last_production_id[3:]) + 1
                            break
                else:
                    increment = 1
            else:
                increment = 1
    except FileNotFoundError:
        increment = 1
    return f"PRD{increment:03d}"

def production_record_keeping(role_id):
    clear_screen()
    print("------Production Record-keeping------")
    print("a. Write Production Record")
    print("b. Display Production Record List")
    print("c. Quit from Production Record-keeping")
    choice = input("ENTER A CHOICE: ")
    if choice == "a":
        write_production_record()
    elif choice == "b":
        production_record = production_record_list()
        view_production_record_list(production_record, role_id)
    elif choice == "c":
        return
    else:
        print("Exiting from Production Record-keeping...")
        return production_record_keeping(role_id)

def display_equipment(equipment):
    print(f"{'ID':<10} {'Equipment Name':<30} {'Functionality':<70} {'Availability':<12}")
    for equipment_id, items in equipment.items():
        for item in items:
            name, functionality, availability, notes = item[1], item[2], item[3], item[4]
            if item[4] != '0':
                print(f"{equipment_id:<10} {name:<30} {functionality:<70} {availability:<12} {notes}")
            else:
                print(f"{equipment_id:<10} {name:<30} {functionality:<70} {availability:<12}")
    return equipment_management_main()
    
def equipment_list():
        equipment = {}
        with open("equipment.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                equipment_id,name,functionality,availability,notes = line.strip().split(',', 4)  # Fixed split to 3
                if equipment_id not in equipment:
                    equipment[equipment_id] = []
                equipment[equipment_id].append((equipment_id,name,functionality,availability,notes))
        return equipment
        
def equipment_detail(data, updated_lines):
    clear_screen()
    print("Select the option to modify equipment detail:")
    print("i. Equipment Name")
    print("ii. Equitment Functionality")
    print("iii. Quit from modification")
    choice = input("ENTER A CHOICE: ")       
    if choice == "i":
        modify_equipment_name(data, updated_lines)
    elif choice == "ii":
        modify_equipment_function(data, updated_lines)
    elif choice == "iii":
        return equipment_management_main()
    else:
        print("invalid option, please try again")
        equipment_detail(data, updated_lines)

def modify_equipment_list():
    modify_equipment_id = input("Enter Equipment ID to modify equipment detail (e.g E001): ")
    updated_lines = []
    found = False
    with open("equipment.txt", "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 4 and modify_equipment_id == data[0]:
                found = True
                print(f"Found equipment: {data[0]} - {data[1]} - {data[2]} - {data[3]}\n")
                equipment_detail(data, updated_lines)
            else:
                updated_lines.append(line)

    if found:
        with open("equipment.txt", "w") as file:
            file.writelines(updated_lines)
        print("Equipment details updated.")
    else:
        print("Equipment ID not found.")

def modify_equipment_name(data, updated_lines):
    print(f"Current Equipment Name: {data[1]}")
    new_equipment_name = input("Enter new equipment name: ")
    data[1] = new_equipment_name
    updated_lines.append(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]}\n")
    print("Equipment name updated.")

def modify_equipment_function(data, updated_lines):
    print(f"Current Equipment Functionality: {data[1]}")
    new_equipment_function = input("Enter new equipment functionality: ")
    data[2] = new_equipment_function
    updated_lines.append(f"{data[0]},{data[1]},{data[2]},{data[3]},{data[4]}\n")
    print("Equipment function updated.")

def add_new_equipment():
    equipment_name = input("Enter new equipment name (0 to cancel): ")
    if equipment_name == '0':
        return equipment_management_main()
    equipment_exists = False
    equipment_id = None

    with open("equipment.txt", "r") as file:
        lines = file.readlines()
        
        for line in lines:
            data = line.strip().split(",")
            if equipment_name.lower() == data[1].lower():  # Case insensitive comparison
                equipment_exists = True
                equipment_id = data[0]
                print(f"Equipment exists with ID: {equipment_id}")
                break

    if not equipment_exists:
        functionality = input(f"Enter {equipment_name} functionality: ")

        new_id = f"E{len(lines) + 1:03d}"  
        new_equipment = f"{new_id},{equipment_name},{functionality},unavailable,new equipment\n"

        with open("equipment.txt", "a") as file:
            file.write(new_equipment)
        print(f"Added new equipment: {equipment_name} with ID: {new_id}")
    equipment_management_main()

def equipment_malfunction_record():
    print("Malfunction Equipment Record")
    malfunction_eqp_id = input("Enter Malfunction Equipment ID: ").strip()
    equipment = equipment_list()
    equipment_found = False

    updated_lines = []
    
    with open("equipment.txt", "r") as file:
        for line in file:
            data = line.strip().split(",", 4)
            if malfunction_eqp_id == data[0]:
                equipment_found = True
                print(f"Equipment found: {data[1]} - {data[2]}")
                data[3] = "unavailable"
                data[4] = "Maintenance Needed"  
                updated_line = ",".join(data)
                updated_lines.append(updated_line + "\n")  # Add updated line
            else:
                updated_lines.append(line)  # Add unmodified line
    
    if equipment_found:
        with open("equipment.txt", "w") as file:
            file.writelines(updated_lines)  # Write all lines back to the file
        print("Record updated successfully.")
    else:
        print("Equipment ID not found.")
    return equipment_management_main()

def equipment_management_main():
    clear_screen()
    print("-----Equiptment Management-----")
    print("a. Display equipment list")
    print("b. Modify equipment")
    print("c. Add New Equipment")
    print("d. Equiptment Malfunction Record")
    print("e. Quit from Equipment Management")
    choice = input("ENTER A CHOICE: ")
    if choice == "a":
        equipment = equipment_list()
        display_equipment(equipment)
        return
    elif choice == "b":
        modify_equipment_list()
    elif choice == "c":   
        add_new_equipment()
    elif choice == "d":
        equipment_malfunction_record()
        return
    elif choice == "e":
        return 
    else:
        print("invalid option, please try again")
        return

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
            baker_main(role_id, user_id)
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

def baker_main(role_id, user_id):
    from Main import main_menu
    while True:
        clear_screen()
        print("===== Welcome to BAKER MENU =====")
        print("1. Manage Recipe")
        print("2. Check Inventory")
        print("3. Production Record-keeping")
        print("4. Equipment Management")
        print("5. Manage Account")
        print("6. Log Out")
        choice = input("ENTER A CHOICE: ")

        if choice == '1':
            manage_recipe_main()
        elif choice == '2':
            inventory_check_main(role_id, user_id)
        elif choice == '3':
            production_record_keeping(role_id)
        elif choice == '4':
            equipment_management_main()
        elif choice == '5':
            account_management(role_id, user_id)
        elif choice == '6':
            print("Log Out Successful...")
            return main_menu()
        else:
            print("Invalid choice. Please try again.")
            return baker_main(role_id, user_id)