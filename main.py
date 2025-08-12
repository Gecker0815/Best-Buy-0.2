import sys
from products import Product, NonStockedProduct, LimitedProduct
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store

product_list = [
    Product("MacBook Air M2", price=1450, quantity=100),
    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    Product("Google Pixel 7", price=500, quantity=250),
    NonStockedProduct("Windows License", price=125),
    LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
]

second_half_price = SecondHalfPrice("Second Half price!")
third_one_free = ThirdOneFree("Third One Free!")
thirty_percent = PercentDiscount("30% off!", percent=30)

product_list[0].promotion = second_half_price
product_list[1].promotion = third_one_free
product_list[3].promotion = thirty_percent

best_buy = Store(product_list)


def show_list_products(store):
    """Displays a formatted list of all products with their special characteristics."""
    products = store.get_all_products()

    for index, product in enumerate(products):
        print(f"{index + 1}. {product.show()}")


def get_valid_choice(length):
    while True:
        choice = input(f"\nChoose an option (1–{length}): ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= length:
                return choice
            else:
                print("Invalid choice. Please select a number within the range.")
        else:
            print("Please enter a valid number.")


def make_order(store):
    """Let user select products and quantities to create an order."""
    products = store.get_all_products()
    max_num = len(products)
    cart = []

    print("\nAvailable products:")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product.show()}")

    while True:
        product_input = get_valid_num("Which product # do you want?: (empty finish)", max_num=max_num)
        if product_input == "":
            break

        selected_product = products[product_input - 1]
        print(f"\n[SELECTED] {selected_product.show()}")

        max_quantity = selected_product.get_quantity()
        product_amount = get_valid_num("Which amount do you want?: ", max_num=max_quantity)

        cart.append((selected_product, product_amount))
        print(f"{product_amount} × {selected_product.name} added to cart!")

    if cart:
        print("\nProcessing your order...\n")
        total_price = 0.0

        for product, quantity in cart:
            try:
                cost = product.buy(quantity)
                total_price += cost
                print(f"{quantity} × {product.name} → {cost:.2f} €")
            except Exception as e:
                print(f"Error buying {product.name}: {e}")

        print(f"\nTotal to pay: {total_price:.2f} €")
    else:
        print("\nOrder cancelled.")


def get_valid_num(query, max_num):
    """Prompt user for a valid number between 1 and max_num."""
    while True:
        value = input(f"{query} (1–{max_num}): ")

        if value == '':
            return ''

        if value.isdigit():
            value = int(value)
            if 1 <= value <= max_num:
                return value
        print("Invalid input. Please enter a valid number.")


def get_valid_float(query):
    """Prompt user for a valid number."""
    while True:
        value = input(f"{query}: ")

        if value == '':
            return ''

        if value.isdigit():
            value = float(value)
            return value

        print("Invalid input. Please enter a valid number.")


def add_product(store):
    """Add a new product to the store via user input."""

    print("\n--- Add New Product ---")

    name = input("Product name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    price = get_valid_float("Product price (€)")

    print("\nProduct type:")
    print("1. Regular product")
    print("2. Non-stocked product")
    print("3. Limited product")

    type_choice = get_valid_choice(3)

    if type_choice == 1:
        quantity = int(get_valid_float("Product quantity"))
        new_product = Product(name, price, quantity)
    elif type_choice == 2:
        new_product = NonStockedProduct(name, price)
    elif type_choice == 3:
        quantity = int(get_valid_float("Product quantity"))
        maximum = int(get_valid_float("Maximum per order"))
        new_product = LimitedProduct(name, price, quantity, maximum)

    promo_choice = choose_promotion()

    if promo_choice == 2:
        new_product.promotion = SecondHalfPrice("Second Half Price")
    elif promo_choice == 3:
        new_product.promotion = ThirdOneFree("Third One Free")
    elif promo_choice == 4:
        percent = get_valid_num("Discount percent", max_num=100)
        new_product.promotion = PercentDiscount(f"{percent}% off", percent)

    store.add_product(new_product)
    print(f"\nProduct '{new_product.name}' added to store!")


def delete_product(store):
    """Delete a product from the store."""
    products = store.get_all_products()

    choice = get_product_choice(products, 'Delete Product')
    selected_product = products[choice - 1]

    confirm = input(f"Are you sure you want to delete '{selected_product.name}'? (y/n): ").lower()
    if confirm == 'y':
        store.products.remove(selected_product)
        print(f"Product '{selected_product.name}' deleted.")
    else:
        print("Deletion cancelled.")


def get_product_choice(products, title, allow_all=False):
    """Let user choose a product from the list. Optionally allow 'All'."""
    if not products:
        print("No products available.")
        return None

    print(f"\n--- {title} ---")
    for i, product in enumerate(products, start=1):
        print(f"{i}. {product.show()}")

    if allow_all:
        print(f"{len(products) + 1}. All products")

    max_choice = len(products) + 1 if allow_all else len(products)
    choice = get_valid_choice(max_choice)

    if allow_all and choice == len(products) + 1:
        return "ALL"
    else:
        return products[choice - 1]


def choose_promotion():
    print("\nAdd promotion?")
    print("1. No promotion")
    print("2. Second Half Price")
    print("3. Third One Free")
    print("4. Percent Discount")

    return get_valid_choice(4)


def change_product_promotion(store):
    """Change product promotion from the store."""
    products = store.get_all_products()
    if not products:
        print("No products in store.")
        return

    choice = get_product_choice(products, 'Change Product Promotion', allow_all=True)

    if choice == "ALL":
        selected_products = products
    else:
        selected_products = [choice]

    promo_choice = choose_promotion()

    confirm = input("Are you sure you want to change the promotion? (y/n): ").lower()
    if confirm != 'y':
        print("Change cancelled.")
        return

    for product in selected_products:
        if promo_choice == 1:
            product.promotion = None
        elif promo_choice == 2:
            product.promotion = SecondHalfPrice("Second Half Price")
        elif promo_choice == 3:
            product.promotion = ThirdOneFree("Third One Free")
        elif promo_choice == 4:
            percent = get_valid_num("Discount percent", max_num=100)
            product.promotion = PercentDiscount(f"{percent}% off", percent)

    print("Promotion updated successfully.")



def run_store_interface(store):
    """Runs the store interface with options to display products, stock and make orders."""

    menu =  {
        "List all products in store": lambda: show_list_products(store),
        "Show total amount in store": lambda: print(f"Total of {store.get_total_quantity()} items in store"),
        "Add product": lambda: add_product(store),
        "Delete product": lambda: delete_product(store),
        "Change product promotion": lambda: change_product_promotion(store),
        "Make an order": lambda: make_order(store),
        "Quit": lambda: sys.exit("Bye!"),
    }

    while True:
        print("\n--- Store Menu ---")
        for i, key in enumerate(menu.keys()):
            print(f"{i+1}. {key}")

        choice = get_valid_choice(len(menu))

        selected_action = menu[list(menu.keys())[choice - 1]]
        selected_action()


def main():
    """Starts the store interface."""
    run_store_interface(best_buy)


if __name__ == '__main__':
    main()
