import logging

from backend.db import migrate_db


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    migrate_db()
    logger.info("migration completed")


if __name__ == "__main__":
    main()
