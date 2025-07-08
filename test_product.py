import pytest
from products import Product
from store import Store

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

def test_product_show_output():
    product = Product("Smartwatch", 199.99, 25)
    display = product.show()
    assert "Smartwatch" in display
    assert "Price: 199.99" in display
    assert "Quantity: 25" in display

def test_product_activate_deactivate_flow():
    product = Product("Speaker", 75, 10)
    product.deactivate()
    assert not product.is_active()
    product.activate()
    assert product.is_active()

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

# ---------------------- Pytest Trigger ----------------------

if __name__ == "__main__":
    result = pytest.main(["-v", "test_product.py"])
    print(f"Exit Code: {result}")
