from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.camera import router as camera
from routers.danh_muc_may_xuc import router as danh_muc_may_xuc
from routers.tong_hop_camera import router as tong_hop_camera
from routers.auth import router as auth
from core.database import Base, engine
import models.danh_muc_may_xuc  # noqa: F401
import models.tong_hop_camera  # noqa: F401
import models.user  # noqa: F401
from routers.danh_muc_may_cao import router as danh_muc_may_cao
import models.danh_muc_may_cao  # noqa: F401
# Create missing tables automatically at startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Camera Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(camera)
app.include_router(danh_muc_may_xuc)
app.include_router(tong_hop_camera)
app.include_router(danh_muc_may_cao)  

@app.get("/")
def root():
    return {"message": "Camera API running"}