from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"


def extract_data():
    """
    Extract raw e-commerce data from CSV files.
    """

    orders = pd.read_csv(DATA_DIR / "orders.csv")
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")

    return orders, customers, products


if __name__ == "__main__":
    orders, customers, products = extract_data()

    print("=== DATA EXTRACTION SUCCESSFUL ===")

    print(f"\nOrders: {len(orders):,} rows")
    print(f"Customers: {len(customers):,} rows")
    print(f"Products: {len(products):,} rows")

    print("\nOrders columns:")
    print(list(orders.columns))

    print("\nCustomers columns:")
    print(list(customers.columns))

    print("\nProducts columns:")
    print(list(products.columns))