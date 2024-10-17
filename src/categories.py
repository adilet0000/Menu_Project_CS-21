import os
from config import POSITIONS_DIR

def get_categories():
    """Get a list of product categories."""
    categories = [d for d in os.listdir(POSITIONS_DIR) if os.path.isdir(os.path.join(POSITIONS_DIR, d))]
    return categories

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
