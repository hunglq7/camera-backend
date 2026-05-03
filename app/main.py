from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers.camera import router as camera
from routers.danh_muc_may_xuc import router as danh_muc_may_xuc
from routers.tong_hop_camera import router as tong_hop_camera
from routers.auth import router as auth
from routers.user import router as user_router
from routers.danh_muc_may_cao import router as danh_muc_may_cao
from routers.danh_muc_dien_thoai import router as danh_muc_dien_thoai
from routers.danh_muc_don_vi import router as danh_muc_don_vi
from routers.danh_muc_camera import router as danh_muc_camera
from routers.upload import router as upload_router
from routers.vi_tri_lap_dat import router as vi_tri_lap_dat
import os

# Note: Database tables are created via Alembic migrations (see run.py)

app = FastAPI(title="Camera Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth)
app.include_router(user_router)
app.include_router(camera)
app.include_router(danh_muc_may_xuc)
app.include_router(tong_hop_camera)
app.include_router(danh_muc_may_cao)
app.include_router(upload_router)
app.include_router(danh_muc_dien_thoai)
app.include_router(danh_muc_don_vi)
app.include_router(danh_muc_camera)
app.include_router(vi_tri_lap_dat)
# Mount static files
# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(project_root, "app", "assets")

# Create assets directory if it doesn't exist
os.makedirs(assets_dir, exist_ok=True)

if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/")
def root():
    return {"message": "Camera API running"}