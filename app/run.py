import os
import uvicorn

if __name__ == "__main__":
    host = os.getenv("HOST", "192.168.0.110")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() == "true"

    uvicorn.run("main:app", host=host, port=port, reload=reload)