class Store:
    """Manages products, stock, and orders for the store."""

    def __init__(self, products=None):
        """Initialize store with optional list of products."""
        if products is None:
            products = []
        self.products = products

    def add_product(self, product):
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        self.products.remove(product)

    def get_total_quantity(self):
        """Return total quantity of all active products."""
        return sum(product.get_quantity() for product in self.products if product.is_active())

    def get_all_products(self):
        """Return list of all active products."""
        return [product for product in self.products if product.is_active()]

    def __contains__(self, item):
        """Check if a product is in the store."""
        return item in self.products

    def order(self, shopping_list):
        """Process an order and return the total price."""
        total_price = 0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price
