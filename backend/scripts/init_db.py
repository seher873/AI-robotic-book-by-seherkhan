"""
Initialize the database by creating all tables
Run this script before starting the application for the first time
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.database import engine, Base
from auth.models import User
from utils.logger import setup_logger

logger = setup_logger("init_db")


def init_db():
    """Create all tables in the database"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✓ Database tables created successfully!")
    logger.info(f"Database URL: {os.getenv('DATABASE_URL', 'sqlite:///./robotic_book.db')}")


if __name__ == "__main__":
    init_db()
