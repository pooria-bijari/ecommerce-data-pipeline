import pandas as pd

from src.transform import (
    clean_orders,
    clean_customers,
    clean_products,
)


def test_orders_have_no_invalid_quantities():
    orders = pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": [1, 2, 3],
        "product_id": [1, 2, 3],
        "order_date": ["2026-01-01"] * 3,
        "quantity": [2, -1, 5],
        "unit_price": [100, 200, 300],
    })

    result = clean_orders(orders)

    assert (result["quantity"] > 0).all()


def test_orders_have_no_missing_customer_ids():
    orders = pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": [1, None, 3],
        "product_id": [1, 2, 3],
        "order_date": ["2026-01-01"] * 3,
        "quantity": [1, 2, 3],
        "unit_price": [100, 200, 300],
    })

    result = clean_orders(orders)

    assert result["customer_id"].notna().all()


def test_orders_have_no_missing_prices():
    orders = pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": [1, 2, 3],
        "product_id": [1, 2, 3],
        "order_date": ["2026-01-01"] * 3,
        "quantity": [1, 2, 3],
        "unit_price": [100, None, 300],
    })

    result = clean_orders(orders)

    assert result["unit_price"].notna().all()


def test_duplicate_orders_are_removed():
    orders = pd.DataFrame({
        "order_id": [1, 1, 2],
        "customer_id": [1, 1, 2],
        "product_id": [1, 1, 2],
        "order_date": ["2026-01-01"] * 3,
        "quantity": [1, 1, 2],
        "unit_price": [100, 100, 200],
    })

    result = clean_orders(orders)

    assert result["order_id"].is_unique


def test_order_total_is_calculated_correctly():
    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [1],
        "product_id": [1],
        "order_date": ["2026-01-01"],
        "quantity": [3],
        "unit_price": [100],
    })

    result = clean_orders(orders)

    assert result.iloc[0]["total_amount"] == 300


def test_customer_ids_are_unique():
    customers = pd.DataFrame({
        "customer_id": [1, 1, 2],
        "first_name": ["John", "John", "Jane"],
        "last_name": ["Doe", "Doe", "Smith"],
        "email": ["a@test.com", "a@test.com", "b@test.com"],
        "country": ["usa", "usa", "uk"],
        "signup_date": ["2026-01-01"] * 3,
    })

    result = clean_customers(customers)

    assert result["customer_id"].is_unique


def test_country_is_normalized():
    customers = pd.DataFrame({
        "customer_id": [1],
        "first_name": ["John"],
        "last_name": ["Doe"],
        "email": ["john@test.com"],
        "country": [" usa "],
        "signup_date": ["2026-01-01"],
    })

    result = clean_customers(customers)

    assert result.iloc[0]["country"] == "USA"


def test_product_prices_are_positive():
    products = pd.DataFrame({
        "product_id": [1, 2, 3],
        "product_name": ["A", "B", "C"],
        "category": ["Home", "Books", "Sports"],
        "unit_price": [100, -50, 200],
    })

    result = clean_products(products)

    assert (result["unit_price"] > 0).all()


def test_product_ids_are_unique():
    products = pd.DataFrame({
        "product_id": [1, 1, 2],
        "product_name": ["A", "A", "B"],
        "category": ["Home", "Home", "Books"],
        "unit_price": [100, 100, 200],
    })

    result = clean_products(products)

    assert result["product_id"].is_unique