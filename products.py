class Product:

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

    def show(self):
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
        if self.quantity - quantity < 0:
            raise ValueError("Not enough stock available to complete this purchase.")
        self.quantity -= quantity
        return float(quantity * self.price)