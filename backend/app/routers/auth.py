from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import verify_password, create_access_token, decode_access_token
from app.models.models import AdminUser
from app.schemas.schemas import AdminLogin, Token, AdminUserOut

router = APIRouter(prefix="/admin", tags=["Admin Authentication"])
security_bearer = HTTPBearer()

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer), 
    db: Session = Depends(get_db)
) -> AdminUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials. Token expired or invalid.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if not email:
        raise credentials_exception
        
    admin = db.query(AdminUser).filter(AdminUser.email == email).first()
    if not admin:
        raise credentials_exception
    return admin

@router.post("/login", response_model=Token)
def login(payload: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.email == payload.email).first()
    if not admin or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    # Generate token
    token = create_access_token(data={"sub": admin.email, "role": admin.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=AdminUserOut)
def get_current_admin_details(admin: AdminUser = Depends(get_current_admin)):
    return admin
