from pathlib import Path
import sys

# ------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from sqlalchemy import text

from src.database import get_engine
from src.logger import get_logger


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

SQL_FILE = BASE_DIR / "sql" / "reporting_views.sql"


# ------------------------------------------------------------
# Logger
# ------------------------------------------------------------

logger = get_logger(__name__)


# ------------------------------------------------------------
# Create reporting views
# ------------------------------------------------------------

def main():

    logger.info("Starting reporting view creation.")

    if not SQL_FILE.exists():
        raise FileNotFoundError(
            f"Reporting SQL file not found: {SQL_FILE}"
        )

    sql_content = SQL_FILE.read_text(
        encoding="utf-8"
    )

    # Execute each statement separately
    statements = [
        statement.strip()
        for statement in sql_content.split(";")
        if statement.strip()
    ]

    engine = get_engine()

    with engine.begin() as connection:

        for i, statement in enumerate(
            statements,
            start=1
        ):

            logger.info(
                f"Executing statement {i}/{len(statements)}"
            )

            connection.execute(
                text(statement)
            )

    logger.info(
        "Reporting views created successfully."
    )

    print()
    print("=" * 70)
    print("REPORTING VIEWS CREATED")
    print("=" * 70)

    print("vw_monthly_revenue")
    print("vw_product_performance")
    print("vw_customer_performance")
    print("vw_country_performance")
    print("vw_daily_sales")


if __name__ == "__main__":
    main()