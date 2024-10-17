import os
from datetime import datetime
from prettytable import PrettyTable
from config import RECIPES_DIR, MENU_FILE, SUMMARY_FILE

def save_order(orders, username, total_price):
    """Save the order in a file named after the user and in menuID.txt."""
    order_file = os.path.join(RECIPES_DIR, f"{username}_order.txt")

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write the order to a separate file in the recipes folder
    with open(order_file, "w", encoding="utf-8") as file:
        file.write(f"Order Receipt - Date: {current_date}\n")
        for product_info, quantity, price in orders:
            file.write(f"{product_info} | Quantity: {quantity} | Price per unit: {price} | Total: {price * quantity}\n")
        
        # Добавляем общую сумму к оплате в конец чека
        file.write(f"\nTotal Amount: {total_price} ")

    # Write the order to the menuID.txt file
    with open(MENU_FILE, "a", encoding="utf-8") as menu_file:
        for product_info, quantity, price in orders:
            menu_file.write(f"{username}: {product_info} Quantity: {quantity} Price per unit: {price} Total: {price * quantity}\n")

    print(f"Order saved in '{order_file}' and added to '{MENU_FILE}'. Total amount: {total_price}")


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
                table.add_row(["", "", ""])
                current_user = username
            
            table.add_row([username, product_details[0], quantity])

        # Write the table to summary.txt
        with open(SUMMARY_FILE, "w", encoding="utf-8") as summary_file:
            summary_file.write(str(table))

        print("\nAll Orders:")
        print(table)
        
        print(f"All orders are also recorded in '{SUMMARY_FILE}'")
    else:
        print("No orders to summarize!")
