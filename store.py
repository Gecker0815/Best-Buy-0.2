class Store:
    """Manages products, stock, and orders for the store."""
    def __init__(self, products=None):
        if products is None:
            products = []
        self.products = products

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_total_quantity(self):
        return sum(product.get_quantity() for product in self.products if product.is_active())

    def get_all_products(self):
        return [product for product in self.products if product.is_active()]

    def __contains__(self, item):
        return item in self.products

    def order(self, shopping_list):
        total_price = 0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price
