import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from promotions import PercentDiscount
from products import Product, NonStockedProduct, LimitedProduct

def test_product_initialization():
    """Test that a Product is initialized correctly."""
    p = Product("Apple", 1.5, 10)
    assert p.name == "Apple"
    assert p.price == 1.5
    assert p.quantity == 10
    assert p.is_active()

def test_product_price_validation():
    """Test that negative prices raise ValueError."""
    with pytest.raises(ValueError):
        Product("Banana", -2, 5)

def test_product_buy_without_promotion():
    """Test buying a product without promotion."""
    p = Product("Orange", 2.0, 10)
    cost = p.buy(3)
    assert cost == 6.0
    assert p.quantity == 7

def test_product_buy_with_promotion():
    """Test buying a product with a 10% discount promotion."""
    p = Product("Mango", 5.0, 10)
    p.promotion = PercentDiscount("10% Off", 10)
    cost = p.buy(2)  # 2 * 5 = 10 → 10 - 10% = 9.0
    assert pytest.approx(cost) == 9.0

def test_product_buy_insufficient_stock():
    """Test that buying more than available stock raises ValueError."""
    p = Product("Pear", 3.0, 2)
    with pytest.raises(ValueError):
        p.buy(5)

def test_non_stocked_product():
    """Test buying a NonStockedProduct."""
    p = NonStockedProduct("Ebook", 10.0)
    cost = p.buy(5)
    assert cost == 50.0

def test_limited_product_buy_within_limit():
    """Test buying a LimitedProduct within the allowed limit."""
    p = LimitedProduct("Concert Ticket", 50.0, 100, 4)
    cost = p.buy(3)
    assert cost == 150.0

def test_limited_product_buy_exceeds_limit():
    """Test that buying more than the limit raises ValueError."""
    p = LimitedProduct("VIP Pass", 100.0, 50, 2)
    with pytest.raises(ValueError):
        p.buy(5)

def test_promotion_type_check():
    """Test that setting an invalid promotion raises TypeError."""
    p = Product("Test", 1.0, 1)
    with pytest.raises(TypeError):
        p.promotion = "NotAPromotion"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
