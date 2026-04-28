from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from services.auth_service import verify_token, get_user_by_id
from models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    Usage in router:
    @app.get("/protected")
    def protected_route(current_user: User = Depends(get_current_user)):
        return {"user": current_user}
    """
    token = credentials.credentials

    try:
        user_id = verify_token(token)
        user = get_user_by_id(db, user_id)
        return user
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
