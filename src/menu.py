import os
from datetime import datetime
from prettytable import PrettyTable

# Absolute path to the positions folder and recipes folder
POSITIONS_DIR = "C:/Users/Username/OneDrive/Рабочий стол/menu/src/positions"
RECIPES_DIR = "recipes"
MENU_FILE = "menuID.txt"
SUMMARY_FILE = "summary.txt"

# Create the recipes folder if it doesn't exist
if not os.path.exists(RECIPES_DIR):
    os.makedirs(RECIPES_DIR)

def get_categories():
    """Get a list of product categories."""
    categories = [d for d in os.listdir(POSITIONS_DIR) if os.path.isdir(os.path.join(POSITIONS_DIR, d))]
    return categories

def get_products(category):
    """Get a list of products from a specific category."""
    category_path = os.path.join(POSITIONS_DIR, category)
    products = [f for f in os.listdir(category_path) if f.endswith(".txt")]
    return products

def display_categories(categories):
    """Display product categories for selection."""
    print("\nAvailable categories:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category.capitalize()}")
    
    while True:
        try:
            choice = int(input("\nChoose a category number (or 0 to exit): ")) - 1
            if choice == -1:
                return None  # User chose to exit
            elif 0 <= choice < len(categories):
                return categories[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def display_products(products):
    """Display a list of products for selection."""
    print("\nAvailable products:")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {os.path.basename(product)}")
    
    while True:
        try:
            choice = int(input("\nChoose a product number (or 0 to finish ordering): ")) - 1
            if choice == -1:
                return None  # User chose to finish ordering
            elif 0 <= choice < len(products):
                return products[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def read_product_info(product_path):
    """Read product information from the file."""
    with open(product_path, "r", encoding="utf-8") as file:
        return file.read().replace("\n", " ")  # Replace new lines with spaces for cohesive output

def save_order(orders, username):
    """Save the order in a file named after the user and in menuID.txt."""
    order_file = os.path.join(RECIPES_DIR, f"{username}_order.txt")
    
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write the order to a separate file in the recipes folder
    with open(order_file, "w", encoding="utf-8") as file:
        file.write(f"Order Receipt - Date: {current_date}\n")
        for product_info, quantity in orders:
            file.write(f"{product_info} | Quantity: {quantity}  ")
    
    # Write the order to the menuID.txt file
    with open(MENU_FILE, "a", encoding="utf-8") as menu_file:
        for product_info, quantity in orders:
            menu_file.write(f"{username}: {product_info} Quantity: {quantity}\n")
    
    print(f"Order saved in '{order_file}' and added to '{MENU_FILE}'.")

def summarize_orders():
    """Function to output all orders to a table using PrettyTable."""
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, "r", encoding="utf-8") as file:
            orders = [order.strip() for order in file.readlines()]

        # Create a PrettyTable object
        table = PrettyTable()
        table.field_names = ["User", "Product Info", "Quantity"]

        # Populate the table with orders
        current_user = None
        for order in orders:
            username, product_info = order.split(": ", 1)
            product_details = product_info.split(" Quantity: ")
            quantity = product_details[1] if len(product_details) > 1 else "N/A"

            # Check if we're still with the same user
            if current_user != username:
                # Add an empty row for spacing before a new user's orders
                table.add_row(["", "", ""])
                current_user = username
            
            table.add_row([username, product_details[0], quantity])

        # Write the table to summary.txt
        with open(SUMMARY_FILE, "w", encoding="utf-8") as summary_file:
            summary_file.write(str(table))  # Convert table to string and write to file

        # Print the table
        print("\nAll Orders:")
        print(table)
        
        print(f"All orders are also recorded in '{SUMMARY_FILE}'")
    else:
        print("No orders to summarize!")

def main():
    """Main function of the program."""
    while True:
        print("\nMenu:")
        print("1. Select and order a product")
        print("2. Summarize orders")
        print("3. Exit")
        command = input("Choose an action (1, 2, or 3): ")

        if command == '1':
            username = input("\nEnter your name to create an order: ")
            orders = []  # Store order information

            while True:
                # Choose a category
                categories = get_categories()
                if not categories:
                    print("No available categories.")
                    break
                
                selected_category = display_categories(categories)
                if selected_category is None:
                    break  # User chose to exit
                
                # Get products in the selected category
                products = get_products(selected_category)
                if not products:
                    print("No available products in this category.")
                    continue
                
                while True:
                    chosen_product = display_products(products)
                    if chosen_product is None:
                        break  # User finished selecting products

                    product_info = read_product_info(os.path.join(POSITIONS_DIR, selected_category, chosen_product))
                    print("\nProduct Information:")
                    print(product_info)

                    # Request quantity of items
                    while True:
                        try:
                            quantity = int(input("Enter quantity for the order: "))
                            if quantity > 0:
                                orders.append((product_info, quantity))
                                print(f"Added: {quantity} pcs.\n")
                                break
                            else:
                                print("Quantity must be a positive number.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    # After entering quantity, ask if the user wants to go back or continue
                    while True:
                        backtrack = input("Do you want to select another product (yes/no)? ").strip().lower()
                        if backtrack in ['yes', 'y']:
                            break  # Go back to product selection
                        elif backtrack in ['no', 'n']:
                            break  # Finish ordering
                        else:
                            print("Please enter 'yes' or 'no'.")
                    
                    if backtrack in ['no', 'n']:
                        break  # Exit product selection loop

            # Save the order if products were selected
            if orders:
                save_order(orders, username)
        
        elif command == '2':
            summarize_orders()
        
        elif command == '3':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
