import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.core.limiter import limiter
from app.core.db import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.models import AdminUser
from app.routers import auth, public, admin

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-stack solar ERP platform backend for SunPlus Power India Pvt. Ltd.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "SunPlus Power Backend is running!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Connect slowapi rate-limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
origins = settings.ALLOWED_ORIGINS
if "*" in origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists and mount it
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Custom validation format: {"error": true, "message": "...", "status_code": ...}
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Clean errors context to ensure JSON serializability
    safe_errors = []
    for err in errors:
        safe_err = err.copy()
        if "ctx" in safe_err:
            safe_err["ctx"] = {k: str(v) for k, v in safe_err["ctx"].items()}
        safe_errors.append(safe_err)
        
    message = "Validation failed: " + "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in errors])
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": message,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "details": safe_errors
        }
    )

# Custom global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    from fastapi import HTTPException
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code
            }
        )
        
    # Log internal error traces
    import traceback
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An internal server error occurred.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

# Include API Routers
app.include_router(auth.router, prefix="/api")
app.include_router(public.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

# Startup hook to automatically create tables and seed admin user
@app.on_event("startup")
def startup_db_seeding():
    # Create all database tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Seed default admin user if none exists
    db = SessionLocal()
    try:
        admin_count = db.query(AdminUser).count()
        if admin_count == 0:
            print("No admin users found. Seeding default administrator account...")
            seed_email = os.getenv("ADMIN_SEED_EMAIL", "admin@sunpluspower.in")
            seed_password = os.getenv("ADMIN_SEED_PASSWORD", "SunPlusAdmin2026!")
            
            hashed_pw = get_password_hash(seed_password)
            default_admin = AdminUser(
                email=seed_email,
                hashed_password=hashed_pw,
                role="admin"
            )
            db.add(default_admin)
            db.commit()
            print(f"Default admin seeded successfully: {seed_email}")
    except Exception as e:
        print(f"Error running database seeding checklist: {str(e)}")
    finally:
        db.close()
# Serve frontend static files (local development fallback)
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

