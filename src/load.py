import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text

# --------------------------------------------------
# Project path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# Imports
# --------------------------------------------------

from src.database import get_engine
from src.logger import get_logger


logger = get_logger(__name__)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data" / "transformed"


# --------------------------------------------------
# Load a single table
# --------------------------------------------------

def load_data(
    df: pd.DataFrame,
    table_name: str,
    engine
):
    """
    Load a DataFrame into an existing PostgreSQL table.

    Existing table structure and foreign keys are preserved.
    """

    logger.info(
        "Loading %d rows into '%s'",
        len(df),
        table_name
    )

    try:

        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False
        )

        logger.info(
            "Successfully loaded %d rows into '%s'",
            len(df),
            table_name
        )

    except Exception:

        logger.exception(
            "Failed to load data into '%s'",
            table_name
        )

        raise


# --------------------------------------------------
# Clear existing data
# --------------------------------------------------

def clear_tables(engine):
    """
    Remove existing table data while preserving
    the database schema and foreign-key relationships.
    """

    logger.info("Clearing existing table data")

    try:

        with engine.begin() as connection:

            connection.execute(
                text(
                    "TRUNCATE TABLE orders, customers, products "
                    "RESTART IDENTITY CASCADE"
                )
            )

        logger.info(
            "Existing table data cleared successfully"
        )

    except Exception:

        logger.exception(
            "Failed to clear existing table data"
        )

        raise


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    logger.info(
        "========== LOAD PROCESS STARTED =========="
    )

    try:

        # ------------------------------------------
        # Check transformed data directory
        # ------------------------------------------

        if not DATA_DIR.exists():

            raise FileNotFoundError(
                f"Transformed data directory not found: {DATA_DIR}"
            )

        logger.info(
            "Looking for transformed data in: %s",
            DATA_DIR
        )

        # ------------------------------------------
        # Expected files
        # ------------------------------------------

        orders_file = DATA_DIR / "orders.csv"
        customers_file = DATA_DIR / "customers.csv"
        products_file = DATA_DIR / "products.csv"

        required_files = [
            orders_file,
            customers_file,
            products_file
        ]

        for file_path in required_files:

            if not file_path.exists():

                raise FileNotFoundError(
                    f"Required file not found: {file_path}"
                )

        logger.info(
            "All transformed CSV files found"
        )

        # ------------------------------------------
        # Read data
        # ------------------------------------------

        logger.info("Reading transformed datasets")

        customers = pd.read_csv(
            customers_file
        )

        products = pd.read_csv(
            products_file
        )

        orders = pd.read_csv(
            orders_file
        )

        logger.info(
            "Customers: %d rows",
            len(customers)
        )

        logger.info(
            "Products: %d rows",
            len(products)
        )

        logger.info(
            "Orders: %d rows",
            len(orders)
        )

        # ------------------------------------------
        # Database connection
        # ------------------------------------------

        logger.info(
            "Creating database connection"
        )

        engine = get_engine()

        logger.info(
            "Database connection established"
        )

        # ------------------------------------------
        # Clear existing data
        # ------------------------------------------

        clear_tables(engine)

        # ------------------------------------------
        # Load parent tables first
        # ------------------------------------------

        logger.info(
            "Loading customers table"
        )

        load_data(
            df=customers,
            table_name="customers",
            engine=engine
        )

        logger.info(
            "Loading products table"
        )

        load_data(
            df=products,
            table_name="products",
            engine=engine
        )

        # ------------------------------------------
        # Load orders last
        # ------------------------------------------

        logger.info(
            "Loading orders table"
        )

        load_data(
            df=orders,
            table_name="orders",
            engine=engine
        )

        # ------------------------------------------
        # Completed
        # ------------------------------------------

        logger.info(
            "========== LOAD PROCESS COMPLETED =========="
        )

    except Exception:

        logger.exception(
            "========== LOAD PROCESS FAILED =========="
        )

        raise


# --------------------------------------------------
# Entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()