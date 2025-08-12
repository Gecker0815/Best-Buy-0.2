import products
import store
import promotions

product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
    products.NonStockedProduct("Windows License", price=125),
    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
]

second_half_price = promotions.SecondHalfPrice("Second Half price!")
third_one_free = promotions.ThirdOneFree("Third One Free!")
thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

product_list[0].promotion = second_half_price
product_list[1].promotion = third_one_free
product_list[3].promotion = thirty_percent

best_buy = store.Store(product_list)

def show_list_products(products):
    """Displays a formatted list of all products with their special characteristics."""
    for index, product in enumerate(products):
        print(f"{index + 1}. {product.show()}")

def run_store_interface(store):
    """Runs the store interface with options to display products, stock and make orders."""
    while True:
        print("\n--- Store Menu ---")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Choose an option (1–4): ")
        print("-----")

        if choice == "1":
            show_list_products(store.get_all_products())

        elif choice == "2":
            print(f"Total of {store.get_total_quantity()} items in store")

        elif choice == "3":
            print("-----")
            print("When you want to finish order, enter empty text.")
            product_num = input("Which product # do you want? ")

            if product_num == "":
                continue

            product_amount = input("Which amount do you want? ")

            if product_amount == "":
                continue

            try:
                selected_product = store.get_all_products()[int(product_num) - 1]
                store.order([(selected_product, int(product_amount))])
                print("Product added to list!")
            except (IndexError, ValueError) as e:
                print(f"Invalid selection: {e}")

        elif choice == "4":
            print("Exiting store. Goodbye!")
            break

def main():
    """Starts the store interface."""
    run_store_interface(best_buy)

if __name__ == '__main__':
    main()
