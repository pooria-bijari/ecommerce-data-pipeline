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

SQL_FILE = BASE_DIR / "sql" / "data_quality.sql"


# ------------------------------------------------------------
# Logger
# ------------------------------------------------------------

logger = get_logger(__name__)


# ------------------------------------------------------------
# Run data quality checks
# ------------------------------------------------------------

def main():

    logger.info("Starting data quality checks.")

    if not SQL_FILE.exists():
        raise FileNotFoundError(
            f"Data quality SQL file not found: {SQL_FILE}"
        )

    sql_content = SQL_FILE.read_text(
        encoding="utf-8"
    )

    queries = [
        query.strip()
        for query in sql_content.split(";")
        if query.strip()
    ]

    engine = get_engine()

    passed = 0
    failed = 0

    for i, query in enumerate(
        queries,
        start=1
    ):

        print()
        print("=" * 70)
        print(f"DATA QUALITY CHECK {i}")
        print("=" * 70)

        try:

            with engine.connect() as connection:

                result = connection.execute(
                    text(query)
                )

                rows = result.fetchall()
                columns = list(result.keys())

            if columns:
                print(" | ".join(columns))
                print("-" * 70)

            if not rows:

                print("PASS - No issues found.")

                passed += 1

            else:

                for row in rows:

                    print(
                        " | ".join(
                            str(value)
                            for value in row
                        )
                    )

                failed += 1

        except Exception as e:

            logger.error(
                f"Data quality check {i} failed: {e}"
            )

            print("CHECK ERROR")
            print(e)

            failed += 1

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("DATA QUALITY SUMMARY")
    print("=" * 70)

    print(f"Total checks: {len(queries)}")
    print(f"Passed:       {passed}")
    print(f"Failed:       {failed}")

    if failed == 0:

        logger.info(
            "All data quality checks passed."
        )

        print()
        print("ALL DATA QUALITY CHECKS PASSED")

    else:

        logger.warning(
            f"{failed} data quality checks found issues."
        )

        print()
        print(
            "DATA QUALITY ISSUES DETECTED"
        )


if __name__ == "__main__":
    main()