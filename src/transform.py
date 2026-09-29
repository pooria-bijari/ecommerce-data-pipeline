import sys
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# Imports
# --------------------------------------------------

from src.extract import extract_data
from src.logger import get_logger


logger = get_logger(__name__)


# --------------------------------------------------
# Cleaning functions
# --------------------------------------------------

def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate the raw orders dataset.
    """

    orders = orders.copy()

    logger.info("Cleaning orders data")

    # Convert dates to proper datetime format
    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    # Remove duplicate orders
    orders = orders.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )

    # Remove orders with missing customer IDs
    orders = orders.dropna(
        subset=["customer_id"]
    )

    # Remove orders with missing prices
    orders = orders.dropna(
        subset=["unit_price"]
    )

    # Remove orders with invalid quantities
    orders = orders[
        orders["quantity"] > 0
    ]

    # Convert IDs and quantity to integers
    orders["customer_id"] = orders["customer_id"].astype(int)
    orders["product_id"] = orders["product_id"].astype(int)
    orders["quantity"] = orders["quantity"].astype(int)

    # Make sure unit price is numeric
    orders["unit_price"] = pd.to_numeric(
        orders["unit_price"],
        errors="coerce"
    )

    # Calculate total order value
    orders["total_amount"] = (
        orders["quantity"] * orders["unit_price"]
    ).round(2)

    logger.info(
        "Orders cleaned: %d rows remaining",
        len(orders)
    )

    return orders


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the customers dataset.
    """

    customers = customers.copy()

    logger.info("Cleaning customers data")

    # Remove duplicate customers
    customers = customers.drop_duplicates(
        subset=["customer_id"],
        keep="first"
    )

    # Convert signup date
    customers["signup_date"] = pd.to_datetime(
        customers["signup_date"],
        errors="coerce"
    )

    # Standardize country names
    customers["country"] = (
        customers["country"]
        .str.strip()
        .str.upper()
    )

    logger.info(
        "Customers cleaned: %d rows remaining",
        len(customers)
    )

    return customers


def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the products dataset.
    """

    products = products.copy()

    logger.info("Cleaning products data")

    # Remove duplicate products
    products = products.drop_duplicates(
        subset=["product_id"],
        keep="first"
    )

    # Standardize text fields
    products["product_name"] = (
        products["product_name"]
        .str.strip()
    )

    products["category"] = (
        products["category"]
        .str.strip()
    )

    # Make sure prices are numeric
    products["unit_price"] = pd.to_numeric(
        products["unit_price"],
        errors="coerce"
    )

    # Remove products with invalid prices
    products = products[
        products["unit_price"] > 0
    ]

    logger.info(
        "Products cleaned: %d rows remaining",
        len(products)
    )

    return products


# --------------------------------------------------
# Transformation
# --------------------------------------------------

def transform_data(orders, customers, products):
    """
    Apply all transformations.
    """

    logger.info("Starting data transformation")

    clean_orders_df = clean_orders(orders)
    clean_customers_df = clean_customers(customers)
    clean_products_df = clean_products(products)

    logger.info("Data transformation completed")

    return (
        clean_orders_df,
        clean_customers_df,
        clean_products_df
    )


# --------------------------------------------------
# Save transformed data
# --------------------------------------------------

def save_transformed_data(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame
):
    """
    Save cleaned datasets as CSV files.
    """

    output_dir = PROJECT_ROOT / "data" / "transformed"

    # Create directory if it doesn't exist
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        "Saving transformed data to: %s",
        output_dir
    )

    # Save orders
    orders_path = output_dir / "orders.csv"

    orders.to_csv(
        orders_path,
        index=False
    )

    logger.info(
        "Saved %d orders to %s",
        len(orders),
        orders_path
    )

    # Save customers
    customers_path = output_dir / "customers.csv"

    customers.to_csv(
        customers_path,
        index=False
    )

    logger.info(
        "Saved %d customers to %s",
        len(customers),
        customers_path
    )

    # Save products
    products_path = output_dir / "products.csv"

    products.to_csv(
        products_path,
        index=False
    )

    logger.info(
        "Saved %d products to %s",
        len(products),
        products_path
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    logger.info("========== TRANSFORM PROCESS STARTED ==========")

    try:

        # ------------------------------------------
        # Extract raw data
        # ------------------------------------------

        logger.info("Extracting raw data")

        orders, customers, products = extract_data()

        logger.info(
            "Raw data loaded: Orders=%d, Customers=%d, Products=%d",
            len(orders),
            len(customers),
            len(products)
        )

        # ------------------------------------------
        # Transform data
        # ------------------------------------------

        clean_orders_df, clean_customers_df, clean_products_df = (
            transform_data(
                orders,
                customers,
                products
            )
        )

        # ------------------------------------------
        # Show transformation statistics
        # ------------------------------------------

        logger.info(
            "Orders removed: %d",
            len(orders) - len(clean_orders_df)
        )

        logger.info(
            "Customers removed: %d",
            len(customers) - len(clean_customers_df)
        )

        logger.info(
            "Products removed: %d",
            len(products) - len(clean_products_df)
        )

        # ------------------------------------------
        # Save transformed data
        # ------------------------------------------

        save_transformed_data(
            clean_orders_df,
            clean_customers_df,
            clean_products_df
        )

        logger.info(
            "========== TRANSFORM PROCESS COMPLETED =========="
        )

    except Exception:

        logger.exception(
            "========== TRANSFORM PROCESS FAILED =========="
        )

        raise


# --------------------------------------------------
# Entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()