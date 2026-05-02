import os
from fastapi import APIRouter, UploadFile, File, status, HTTPException
from datetime import datetime
import aiofiles
from pathlib import Path

router = APIRouter(prefix="/upload", tags=["File Upload"])

# Get the project root directory and create assets/avatar directory if it doesn't exist
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_DIR = os.path.join(project_root, "app", "assets", "avatar")
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.post("/avatar", status_code=status.HTTP_200_OK)
async def upload_avatar(file: UploadFile = File(...)):
    """Upload user avatar image"""
    try:
        # Check file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Read file content once
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"avatar_{timestamp}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Verify file was saved
        if not os.path.exists(file_path):
            raise Exception(f"File was not saved to {file_path}")

        # Return relative path for storage in database (without leading slash)
        relative_path = f"assets/avatar/{filename}"
        return {"filename": relative_path, "message": "Avatar uploaded successfully"}

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_msg = f"Failed to upload file: {str(e)}"
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg
        )
