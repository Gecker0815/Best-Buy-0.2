import products
import store

# setup initial stock of inventory
product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                 products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 products.Product("Google Pixel 7", price=500, quantity=250)
               ]
best_buy = store.Store(product_list)


def start(store):
    while True:
        print("\n--- Store Menu ---")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Choose an option (1–4): ")

        print("-----")

        if choice == "1" or choice == "3":
            for index, product in enumerate(store.get_all_products()):
                print(f"{index + 1}. {product.show()}")

        if choice == "2":
            print(f"Total of {store.get_total_quantity()} items in store")

        if choice == "3":
            print("-----")
            print("When you want to finish order, enter empty text.")
            product_num = input("Which product # do you want? ")

            if product_num == "":
                continue

            product_amount = input("Which amount do you want? ")

            if product_num == "":
                continue

            store.order([(product_list[int(product_num) - 1], int(product_amount))])

            print("Product added to list!")

        if choice == "4":
            break


start(best_buy)