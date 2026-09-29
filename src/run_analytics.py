from pathlib import Path
import sys

# ------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

from sqlalchemy import text

from src.database import get_engine
from src.logger import get_logger


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

SQL_FILE = BASE_DIR / "sql" / "analytics.sql"


# ------------------------------------------------------------
# Logger
# ------------------------------------------------------------

logger = get_logger(__name__)


# ------------------------------------------------------------
# Run analytics
# ------------------------------------------------------------

def main():

    logger.info("Starting analytics execution.")

    if not SQL_FILE.exists():
        raise FileNotFoundError(
            f"Analytics SQL file not found: {SQL_FILE}"
        )

    sql_content = SQL_FILE.read_text(encoding="utf-8")

    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip()
    ]

    logger.info(
        f"Found {len(queries)} analytics queries."
    )

    engine = get_engine()

    successful_queries = 0
    failed_queries = 0

    for i, query in enumerate(queries, start=1):

        logger.info(
            f"Running analytics query {i}/{len(queries)}"
        )

        print("\n" + "=" * 70)
        print(f"QUERY {i}")
        print("=" * 70)

        try:

            # ------------------------------------------------
            # Each query gets its own transaction
            # ------------------------------------------------

            with engine.begin() as connection:

                result = connection.execute(
                    text(query)
                )

                rows = result.fetchall()
                columns = list(result.keys())

            # ------------------------------------------------
            # Print results
            # ------------------------------------------------

            if columns:
                print(" | ".join(columns))
                print("-" * 70)

            for row in rows:
                print(
                    " | ".join(
                        str(value)
                        for value in row
                    )
                )

            successful_queries += 1

        except Exception as e:

            failed_queries += 1

            logger.error(
                f"Query {i} failed: {e}"
            )

            print("\nQUERY FAILED")
            print("-" * 70)
            print(e)

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("ANALYTICS SUMMARY")
    print("=" * 70)

    print(f"Total queries:      {len(queries)}")
    print(f"Successful queries: {successful_queries}")
    print(f"Failed queries:     {failed_queries}")

    if failed_queries == 0:

        logger.info(
            "All analytics queries completed successfully."
        )

    else:

        logger.warning(
            f"{failed_queries} analytics queries failed."
        )


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

if __name__ == "__main__":
    main()