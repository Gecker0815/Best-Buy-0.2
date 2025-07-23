# 🛍️ Python Store System

This project is a modular store system built in Python that allows users to interact via a terminal interface. Products can be purchased, promotions can be applied, and stock is managed dynamically.

---

## 📦 Features

- Add multiple types of products (stocked, non-stocked, limited)
- Apply custom promotions like:
  - **Second Half Price**
  - **Buy Two, Get One Free**
  - **Percentage Discount**
- Interactive store menu to:
  - List available products
  - View total stock
  - Place product orders with automatic discount calculation

---

## 🧩 Code Structure

| File/Module     | Description                                      |
|----------------|--------------------------------------------------|
| `main.py`       | Entry point. Runs the store interface           |
| `store.py`      | Defines the `Store` class for managing inventory and orders |
| `products.py`   | Defines multiple product types and handles purchase logic |
| `promotions.py` | Contains promotion logic and pricing algorithms |

---

## 🚀 How to Run

1. Clone this repo
2. Make sure all `.py` files are in the same directory
3. Run the store interface:

```bash
python main.py
```

---

## 🎁 Example Products

```python
products.Product("MacBook Air M2", price=1450, quantity=100)
products.NonStockedProduct("Windows License", price=125)
products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
```

---

## 🔖 Adding Promotions

Promotions can be assigned like so:

```python
macbook.promotion = promotions.SecondHalfPrice("Second Half Price!")
license.promotion = promotions.PercentDiscount("30% off!")
```

During checkout, the pricing logic will automatically apply any active promotion.
