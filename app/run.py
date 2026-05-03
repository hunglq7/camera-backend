import os
import sys
import subprocess
import uvicorn
from pathlib import Path

if __name__ == "__main__":
    # Create assets directory
    assets_dir = Path("/app/assets/avatar")
    assets_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created assets directory: {assets_dir}", flush=True)
    
    # Ensure database migrations are run
    try:
        print("\n" + "="*50, flush=True)
        print("Running database migrations...", flush=True)
        print("="*50, flush=True)
        # Get the project root (this file lives in /app/run.py inside container)
        project_root = Path(__file__).parent  # /app
        alembic_ini = project_root / "alembic.ini"
        
        print(f"Project root: {project_root}", flush=True)
        print(f"Alembic config: {alembic_ini}", flush=True)
        print(f"Alembic config exists: {alembic_ini.exists()}", flush=True)
        
        os.chdir(project_root)
        
        # Step 1: Apply migrations
        # Note: Do not auto-generate migrations during app startup.
        # Migrations should be created manually with alembic revision --autogenerate.
        print("\nStep 1: Applying migrations...", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "-c", str(alembic_ini), "upgrade", "head"],
            cwd=str(project_root),
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        if result.returncode != 0:
            print(f"Error: Migration failed with code {result.returncode}", flush=True)
        else:
            print("Migrations completed successfully", flush=True)
        print("="*50 + "\n", flush=True)
    except Exception as e:
        print(f"Error: Could not run migrations: {e}", flush=True)
        import traceback
        traceback.print_exc()
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "False").lower() == "true"

    print(f"Starting FastAPI server on {host}:{port}", flush=True)
    uvicorn.run("main:app", host=host, port=port, reload=reload)