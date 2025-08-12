from promotions import Promotion

class Product:
    """A store product with name, price, quantity, and optional promotion."""

    def __init__(self, name, price, quantity):
        """Initialize product with name, price, and quantity."""
        if not isinstance(name, str):
            raise TypeError("Name must be of type str")
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number (int or float)")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be of type int")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self._promotion = None

    @property
    def price(self):
        """Get the product's price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the product's price with validation."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = value

    def __lt__(self, other):
        """Compare products by price (less than)."""
        return self.price < other.price

    def __gt__(self, other):
        """Compare products by price (greater than)."""
        return self.price > other.price

    @property
    def promotion(self):
        """Get the current promotion."""
        return self._promotion

    @promotion.setter
    def promotion(self, promotion):
        """Set a promotion for the product."""
        if not isinstance(promotion, Promotion) and promotion is not None:
            raise TypeError("promotion must be an instance of Promotion or None")
        self._promotion = promotion

    def get_quantity(self):
        """Return current quantity in stock."""
        return self.quantity

    def set_quantity(self, quantity):
        """Update the product's quantity."""
        self.quantity = quantity

    def is_active(self):
        """Check if the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def __str__(self):
        """Return string representation of the product."""
        return self.show()

    def show(self):
        """Return detailed product info including promotion."""
        base = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotion:
            base += f", Promotion: {self.promotion}"
        return base

    def buy(self, quantity):
        """Buy a quantity of the product, applying promotion if available."""
        if self.quantity - quantity < 0:
            raise ValueError("Not enough stock available to complete this purchase.")

        self.quantity -= quantity

        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        else:
            return float(quantity * self.price)


class NonStockedProduct(Product):
    """Product without stock limits, always available."""

    def __init__(self, name, price):
        """Initialize a non-stocked product with name and price."""
        super().__init__(name, price, 0)

    def show(self):
        """Return info indicating it's a non-stocked item."""
        return f"{super().show()} [Non-stocked item]"

    def buy(self, quantity):
        """Buy any quantity of the non-stocked product."""
        return float(quantity * self.price)


class LimitedProduct(Product):
    """Product with a maximum purchase limit per order."""

    def __init__(self, name, price, quantity, maximum):
        """Initialize limited product with name, price, quantity, and max limit."""
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self):
        """Return info including the purchase limit."""
        return f"{super().show()} [Limit: {self.maximum} per order]"

    def buy(self, quantity):
        """Buy product with enforcement of maximum limit."""
        if quantity > self.maximum:
            raise ValueError(f"Cannot buy more than {self.maximum} units.")
        return super