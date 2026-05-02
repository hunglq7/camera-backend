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
        
        # Step 1: Auto-generate migration if there are model changes
        print("\nStep 1: Detecting model changes...", flush=True)
        revision_result = subprocess.run(
            [sys.executable, "-m", "alembic", "-c", str(alembic_ini), "revision", "--autogenerate", "-m", "auto_migration"],
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if revision_result.returncode == 0:
            print("Migration file generated (if changes detected)", flush=True)
            print(revision_result.stdout, flush=True)
        else:
            print(f"Note: {revision_result.stderr}", flush=True)
        
        # Step 2: Apply migrations
        print("\nStep 2: Applying migrations...", flush=True)
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