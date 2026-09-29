from pathlib import Path
import sys

# ------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from sqlalchemy import inspect

from src.database import get_engine


def main():

    engine = get_engine()
    inspector = inspect(engine)

    tables = [
        "customers",
        "products",
        "orders"
    ]

    for table in tables:

        print("\n" + "=" * 60)
        print(f"TABLE: {table}")
        print("=" * 60)

        columns = inspector.get_columns(table)

        for column in columns:

            print(
                f"{column['name']} "
                f"| {column['type']} "
                f"| nullable={column['nullable']}"
            )


if __name__ == "__main__":
    main()