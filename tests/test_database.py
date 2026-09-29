from sqlalchemy import text

from src.database import get_engine


def test_customers_count():
    engine = get_engine()

    with engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM customers")
        ).scalar()

    assert count == 1000


def test_products_count():
    engine = get_engine()

    with engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar()

    assert count == 100


def test_orders_count():
    engine = get_engine()

    with engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM orders")
        ).scalar()

    assert count == 9900


def test_customer_ids_are_unique():
    engine = get_engine()

    with engine.connect() as connection:
        duplicates = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM (
                    SELECT customer_id
                    FROM customers
                    GROUP BY customer_id
                    HAVING COUNT(*) > 1
                ) AS duplicate_customers
                """
            )
        ).scalar()

    assert duplicates == 0


def test_product_ids_are_unique():
    engine = get_engine()

    with engine.connect() as connection:
        duplicates = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM (
                    SELECT product_id
                    FROM products
                    GROUP BY product_id
                    HAVING COUNT(*) > 1
                ) AS duplicate_products
                """
            )
        ).scalar()

    assert duplicates == 0


def test_order_ids_are_unique():
    engine = get_engine()

    with engine.connect() as connection:
        duplicates = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM (
                    SELECT order_id
                    FROM orders
                    GROUP BY order_id
                    HAVING COUNT(*) > 1
                ) AS duplicate_orders
                """
            )
        ).scalar()

    assert duplicates == 0


def test_orders_have_valid_customers():
    engine = get_engine()

    with engine.connect() as connection:
        orphan_orders = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM orders o
                LEFT JOIN customers c
                    ON o.customer_id = c.customer_id
                WHERE c.customer_id IS NULL
                """
            )
        ).scalar()

    assert orphan_orders == 0


def test_orders_have_valid_products():
    engine = get_engine()

    with engine.connect() as connection:
        orphan_orders = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM orders o
                LEFT JOIN products p
                    ON o.product_id = p.product_id
                WHERE p.product_id IS NULL
                """
            )
        ).scalar()

    assert orphan_orders == 0