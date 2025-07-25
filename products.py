from promotions import Promotion

class Product:
    """Represents a product in the store."""
    def __init__(self, name, price, quantity):
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
        self._promotion  = None

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = value

    def __lt__(self, other):
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price

    @property
    def promotion(self):
        return self._promotion

    @promotion.setter
    def promotion(self, promotion):
        if not isinstance(promotion, Promotion) and promotion is not None:
            raise TypeError("promotion must be an instance of Promotion or None")
        self._promotion = promotion

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity

    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def __str__(self):
        if self.promotion:
            return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Promotion: {self._promotion}"
        else:
            return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
        if self.quantity - quantity < 0:
            raise ValueError("Not enough stock available to complete this purchase.")

        self.quantity -= quantity

        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        else:
            return float(quantity * self.price)


class NonStockedProduct(Product):
    """Represents a non-stocked product that can be bought without limit."""
    def __init__(self, name, price):
        super().__init__(name, price, 0)
        pass

    def __str__(self):
        return f"{self.name}, Price: {self.price}"

    def buy(self, quantity):
        return float(quantity * self.price)


class LimitedProduct(Product):
    """Represents a limited quantity product with a maximum purchase limit."""
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum
        pass

    def __str__(self):
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum:{self.maximum}"

    def buy(self, quantity):
        if quantity > self.maximum:
            raise ValueError(f"Cannot buy more than {self.maximum} units.")
        return super().buy(quantity)