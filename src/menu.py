from categories import get_categories, display_categories
from products import get_products, display_products, read_product_info
from orders import save_order, summarize_orders

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
            total_price = 0  # Добавляем переменную для общей суммы

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

                    product_info, price = read_product_info(selected_category, chosen_product)
                    print("\nProduct Information:")
                    print(product_info)

                    # Request quantity of items
                    while True:
                        try:
                            quantity = int(input("Enter quantity for the order: "))
                            if quantity > 0:
                                orders.append((product_info, quantity, price))
                                total_price += price * quantity  # Увеличиваем общую сумму заказа
                                print(f"Added: {quantity} pcs.\n")
                                break
                            else:
                                print("Quantity must be a positive number.")
                        except ValueError:
                            print("Please enter a valid number.")
                    
                    backtrack = input("Do you want to select another product (yes/no)? ").strip().lower()
                    if backtrack in ['no', 'n']:
                        break  # Exit product selection loop

            # Save the order if products were selected
            if orders:
                save_order(orders, username, total_price)
        
        elif command == '2':
            summarize_orders()
        
        elif command == '3':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
