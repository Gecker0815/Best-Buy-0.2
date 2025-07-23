from abc import ABC, abstractmethod

class Promotion(ABC):
    """Abstract base class for all promotion types."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    @abstractmethod
    def apply_promotion(product, quantity):
        raise NotImplementedError("This method must be overridden by subclasses.")


class SecondHalfPrice(Promotion):
    """Applies half price to every second item."""

    def apply_promotion(self, product, quantity):
        full_items = quantity // 2
        half_items = quantity - full_items
        return full_items * product.price + half_items * (product.price / 2)


class ThirdOneFree(Promotion):
    """Applies a 'buy two, get one free' promotion."""

    def apply_promotion(self, product, quantity):
        free_items = quantity // 3
        paid_items = quantity - free_items
        return paid_items * product.price


class PercentDiscount(Promotion):
    """Applies a percentage-based discount to the total price."""

    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity):
        total = product.price * quantity
        discount = total * (self.percent / 100)
        return total - discount
