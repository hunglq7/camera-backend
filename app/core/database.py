from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import SQLALCHEMY_DATABASE_URL, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
import urllib.parse

safe_password = urllib.parse.quote_plus(DB_PASSWORD)

def ensure_database_exists():
    tmp_url = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}"
    tmp_engine = create_engine(tmp_url)

    with tmp_engine.connect() as conn:
        conn.execute(text(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        ))
        conn.execute(text("commit"))

    tmp_engine.dispose()


# ensure_database_exists()  # Commented out to avoid connection issues during startup

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,  # Tăng từ 5 (mặc định) lên 20
    max_overflow=40,  # Tăng từ 10 (mặc định) lên 40
    pool_pre_ping=True,
    pool_recycle=3600
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()