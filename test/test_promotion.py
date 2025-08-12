import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from products import Product
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount

def test_second_half_price_promotion():
    """Test 'SecondHalfPrice' promotion: every second item is half price."""
    p = Product("Socks", 10.0, 10)
    p.promotion = SecondHalfPrice("Second Half Price")
    cost = p.buy(4)  # 2 full price + 2 half price = 20 + 10 = 30
    assert cost == 30.0

def test_third_one_free_promotion():
    """Test 'ThirdOneFree' promotion: buy 3, pay for 2."""
    p = Product("Notebook", 15.0, 9)
    p.promotion = ThirdOneFree("Buy 2 Get 1 Free")
    cost = p.buy(6)  # 2 free, pay for 4 = 4 * 15 = 60
    assert cost == 60.0

def test_percent_discount_promotion():
    """Test 'PercentDiscount' promotion: 20% off total price."""
    p = Product("Backpack", 50.0, 5)
    p.promotion = PercentDiscount("20% Off", 20)
    cost = p.buy(2)  # 100 - 20% = 80
    assert cost == 80.0

if __name__ == "__main__":
    pytest.main(["-v", __file__])
