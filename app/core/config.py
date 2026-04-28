import os
import urllib.parse

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "LeHung@79")
DB_HOST = os.getenv("DB_HOST", "192.168.0.110")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "camera_management")

safe_password = urllib.parse.quote_plus(DB_PASSWORD)

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{safe_password}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "nkxnzcfsdhfdshfhdsdl3433i46546jkjdljdsjdfgdsf321564")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7