from pathlib import Path
import random

import numpy as np
import pandas as pd
from faker import Faker


fake = Faker()

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(n=1000):
    customers = []

    for customer_id in range(1, n + 1):
        customers.append(
            {
                "customer_id": customer_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "country": random.choice(
                    ["USA", "UK", "Germany", "France", "Canada", "Australia"]
                ),
                "signup_date": fake.date_between(
                    start_date="-3y",
                    end_date="today",
                ),
            }
        )

    return pd.DataFrame(customers)


def generate_products(n=100):
    categories = [
        "Electronics",
        "Home",
        "Clothing",
        "Books",
        "Sports",
        "Beauty",
    ]

    products = []

    for product_id in range(1, n + 1):
        products.append(
            {
                "product_id": product_id,
                "product_name": fake.catch_phrase(),
                "category": random.choice(categories),
                "unit_price": round(random.uniform(10, 1000), 2),
            }
        )

    return pd.DataFrame(products)


def generate_orders(n=10000, customer_count=1000, product_count=100):
    orders = []

    for order_id in range(1, n + 1):
        orders.append(
            {
                "order_id": order_id,
                "customer_id": random.randint(1, customer_count),
                "product_id": random.randint(1, product_count),
                "order_date": fake.date_between(
                    start_date="-1y",
                    end_date="today",
                ),
                "quantity": random.randint(1, 5),
                "unit_price": round(random.uniform(10, 1000), 2),
            }
        )

    return pd.DataFrame(orders)


def introduce_data_quality_issues(orders):
    """
    Introduce realistic problems into raw transactional data.
    """

    # Missing customer IDs
    missing_indices = np.random.choice(
        orders.index,
        size=50,
        replace=False,
    )

    orders.loc[missing_indices, "customer_id"] = np.nan

    # Invalid quantities
    invalid_indices = np.random.choice(
        orders.index,
        size=20,
        replace=False,
    )

    orders.loc[invalid_indices, "quantity"] = -1

    # Missing prices
    price_indices = np.random.choice(
        orders.index,
        size=30,
        replace=False,
    )

    orders.loc[price_indices, "unit_price"] = np.nan

    # Duplicate records
    duplicates = orders.sample(
        25,
        random_state=RANDOM_SEED,
    )

    orders = pd.concat(
        [orders, duplicates],
        ignore_index=True,
    )

    return orders


def main():
    print("Generating customers...")
    customers = generate_customers()

    print("Generating products...")
    products = generate_products()

    print("Generating orders...")
    orders = generate_orders()

    print("Introducing data-quality issues...")
    orders = introduce_data_quality_issues(orders)

    customers.to_csv(
        OUTPUT_DIR / "customers.csv",
        index=False,
    )

    products.to_csv(
        OUTPUT_DIR / "products.csv",
        index=False,
    )

    orders.to_csv(
        OUTPUT_DIR / "orders.csv",
        index=False,
    )

    print("\nData generation complete.")
    print(f"Customers: {len(customers):,}")
    print(f"Products: {len(products):,}")
    print(f"Orders: {len(orders):,}")


if __name__ == "__main__":
    main()