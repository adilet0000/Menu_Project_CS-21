import os
from config import POSITIONS_DIR

def get_products(category):
    """Get a list of products from a specific category."""
    category_path = os.path.join(POSITIONS_DIR, category)
    products = [f for f in os.listdir(category_path) if f.endswith(".txt")]
    return products

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

def read_product_info(category, product):
    """Read product information from the file."""
    product_path = os.path.join(POSITIONS_DIR, category, product)
    with open(product_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    product_info = " ".join([line.strip() for line in lines if not line.startswith("Price:")])
    price_line = next((line for line in lines if line.startswith("Price:")), None)

    if price_line:
        price = float(price_line.split(":")[1].strip())
    else:
        price = 0.0

    return product_info, price
