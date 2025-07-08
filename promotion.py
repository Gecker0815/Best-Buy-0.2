from abc import ABC, abstractmethod

class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(product, quantity):
        raise NotImplementedError("This method must be overridden by subclasses.")


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity):
        full_items = quantity // 2
        half_items = quantity - full_items
        return full_items * product.price + half_items * (product.price / 2)


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity):
        free_items = quantity // 3
        paid_items = quantity - free_items
        return paid_items * product.price


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity):
        total = product.price * quantity
        discount = total * (self.percent / 100)
        return total - discount
