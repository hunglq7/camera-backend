import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)


def run_migrations():
    """
    Run Alembic migrations.
    
    Alembic is a database migration tool that tracks schema changes.
    This replaces the previous metadata.create_all() approach.
    """
    print("Running Alembic migrations...")
    
    # Change to project root directory
    os.chdir(PROJECT_ROOT)
    
    # Run alembic upgrade head
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        capture_output=False
    )
    
    if result.returncode == 0:
        print("✓ Migration completed successfully!")
    else:
        print("✗ Migration failed!")
        sys.exit(1)


if __name__ == "__main__":
    run_migrations()

