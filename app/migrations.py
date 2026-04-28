import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.database import Base, engine
import models.camera  # noqa: F401
import models.danh_muc_may_xuc  # noqa: F401
import models.tong_hop_camera  # noqa: F401
import models.danh_muc_may_cao  # noqa: F401

def run_migrations():
    Base.metadata.create_all(bind=engine)
    print("Migration completed. Tables:", list(Base.metadata.tables.keys()))


if __name__ == "__main__":
    run_migrations()
