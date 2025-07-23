import pytest
from products import Product, NonStockedProduct, LimitedProduct
from store import Store
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount

# ---------------------- Product Tests ----------------------

def test_create_normal_product():
    product = Product("Laptop", 999.99, 10)
    assert product.name == "Laptop"
    assert product.price == 999.99
    assert product.quantity == 10
    assert product.is_active()

def test_create_product_with_invalid_details():
    with pytest.raises(TypeError):
        Product("", "not-a-price", 10)
    with pytest.raises(TypeError):
        Product("Mouse", -25.5, "ten")

def test_product_becomes_inactive_when_quantity_zero():
    product = Product("Keyboard", 50, 1)
    product.buy(1)
    assert product.get_quantity() == 0
    product.deactivate()
    assert not product.is_active()

def test_product_purchase_changes_quantity_and_returns_price():
    product = Product("Monitor", 200, 5)
    price = product.buy(2)
    assert price == 400
    assert product.get_quantity() == 3

def test_buy_more_than_available_quantity_raises_exception():
    product = Product("Headphones", 150, 2)
    with pytest.raises(ValueError):
        product.buy(3)

def test_set_quantity_updates_correctly():
    product = Product("Tablet", 300, 10)
    product.set_quantity(5)
    assert product.get_quantity() == 5

def test_product_output():
    product = Product("Smartwatch", 199.99, 25)
    display = str(product)
    assert "Smartwatch" in display
    assert "Price: 199.99" in display
    assert "Quantity: 25" in display

def test_product_activate_deactivate_flow():
    product = Product("Speaker", 75, 10)
    product.deactivate()
    assert not product.is_active()
    product.activate()
    assert product.is_active()

# ---------------------- Price Property & Comparison Tests ----------------------

def test_price_property_allows_valid_value():
    product = Product("Router", 120, 10)
    product.price = 150
    assert product.price == 150

def test_price_property_raises_error_on_negative_value():
    product = Product("Router", 120, 10)
    with pytest.raises(ValueError):
        product.price = -10

def test_product_comparison_lt():
    p1 = Product("Basic Phone", 300, 5)
    p2 = Product("Smartphone", 800, 5)
    assert p1 < p2
    assert not p2 < p1

def test_product_comparison_gt():
    p1 = Product("Basic Phone", 300, 5)
    p2 = Product("Smartphone", 800, 5)
    assert p2 > p1
    assert not p1 > p2

# ---------------------- NonStockedProduct Tests ----------------------

def test_non_stocked_product_has_zero_quantity():
    product = NonStockedProduct("Streaming Subscription", 9.99)
    assert product.get_quantity() == 0
    assert product.is_active()

def test_non_stocked_product_buy_does_not_change_quantity():
    product = NonStockedProduct("Streaming Subscription", 9.99)
    price = product.buy(1)
    assert price == 9.99
    assert product.get_quantity() == 0

def test_non_stocked_product_output():
    product = NonStockedProduct("eBook", 5.49)
    display = str(product)
    assert "eBook" in display
    assert "Price: 5.49" in display
    assert "Quantity" not in display

# ---------------------- LimitedProduct Tests ----------------------

def test_limited_product_respects_maximum_quantity():
    product = LimitedProduct("Concert Ticket", 120.0, 10, 2)
    with pytest.raises(ValueError):
        product.buy(3)

def test_limited_product_buy_within_maximum():
    product = LimitedProduct("Concert Ticket", 120.0, 10, 3)
    price = product.buy(2)
    assert price == 240.0
    assert product.get_quantity() == 8

def test_limited_product_output_contains_maximum():
    product = LimitedProduct("VIP Pass", 199.99, 5, 1)
    display = str(product)
    assert "VIP Pass" in display
    assert "Price: 199.99" in display
    assert "Quantity: 5" in display
    assert "Maximum:1" in display

# ---------------------- Store Tests ----------------------

def test_store_initialization_and_total_quantity():
    p1 = Product("Camera", 300, 2)
    p2 = Product("Tripod", 50, 3)
    shop = Store([p1, p2])
    assert shop.get_total_quantity() == 5

def test_get_all_products_returns_only_active():
    p1 = Product("Camera", 300, 2)
    p2 = Product("Tripod", 50, 3)
    p2.deactivate()
    shop = Store([p1, p2])
    active_products = shop.get_all_products()
    assert len(active_products) == 1
    assert active_products[0].name == "Camera"

def test_store_add_and_remove_product():
    p = Product("Microphone", 100, 5)
    shop = Store()
    shop.add_product(p)
    assert p in shop.products
    shop.remove_product(p)
    assert p not in shop.products

def test_store_order_reduces_quantity_and_returns_total_price():
    p = Product("Speaker", 200, 4)
    shop = Store([p])
    total_price = shop.order([(p, 2)])
    assert total_price == 400
    assert p.get_quantity() == 2

def test_store_order_raises_error_on_invalid_quantity():
    p = Product("Mixer", 500, 1)
    shop = Store([p])
    with pytest.raises(ValueError):
        shop.order([(p, 2)])

def test_order_with_multiple_products():
    p1 = Product("Phone", 800, 2)
    p2 = Product("Charger", 20, 5)
    store = Store([p1, p2])
    total = store.order([(p1, 1), (p2, 3)])
    assert total == 800 + 60
    assert p1.get_quantity() == 1
    assert p2.get_quantity() == 2

def test_store_contains_product_true():
    p1 = Product("Camera", 500, 2)
    shop = Store([p1])
    assert p1 in shop

def test_store_contains_product_false():
    p1 = Product("Camera", 500, 2)
    p2 = Product("Tripod", 80, 4)
    shop = Store([p1])
    assert p2 not in shop

# ---------------------- Promotion Tests ----------------------

def test_buy_with_percent_discount():
    product = Product("Sunglasses", 100, 5)
    discount = PercentDiscount("30% Off", percent=30)
    product.promotion = discount
    result = product.buy(2)
    assert result == 140.0
    assert product.get_quantity() == 3

def test_buy_with_third_one_free():
    product = Product("Notebook", 20, 9)
    promo = ThirdOneFree("Buy 2, get 1 free")
    product.promotion = promo
    result = product.buy(3)
    assert result == 40.0
    assert product.get_quantity() == 6

def test_buy_with_second_half_price():
    product = Product("T-Shirt", 50, 4)
    promo = SecondHalfPrice("Second item half off")
    product.promotion = promo
    result = product.buy(2)
    assert result == 75.0
    assert product.get_quantity() == 2

def test_buy_exact_quantity_for_third_one_free():
    product = Product("Notebook", 20, 6)
    promo = ThirdOneFree("Buy 2, get 1 free")
    product.promotion = promo
    result = product.buy(6)
    assert result == 80.0
    assert product.get_quantity() == 0

def test_second_half_price_with_odd_quantity():
    product = Product("T-Shirt", 50, 5)
    promo = SecondHalfPrice("Second item half off")
    product.promotion = promo
    result = product.buy(5)
    assert result == 175.0
    assert product.get_quantity() == 0

def test_percent_discount_full_coverage():
    product = Product("Sticker Pack", 10, 10)
    promo = PercentDiscount("100% Off", percent=100)
    product.promotion = promo
    result = product.buy(2)
    assert result == 0.0
    assert product.get_quantity() == 8

def test_buy_without_promotion():
    product = Product("Mug", 10, 5)
    result = product.buy(2)
    assert result == 20.0
    assert product.get_quantity() == 3

def test_setting_invalid_promotion_type_raises():
    product = Product("Lamp", 60, 5)
    with pytest.raises(TypeError):
        product.promotion = "Not a promotion"

# ---------------------- Pytest Trigger ----------------------

if __name__ == "__main__":
    result = pytest.main(["-v", "test_product.py"])
    print(f"Exit Code: {result}")
