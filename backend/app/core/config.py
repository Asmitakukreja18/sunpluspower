import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the backend folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "SunPlus Power India Platform")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    
    # CORS
    ALLOWED_ORIGINS: list = [
        origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",") if origin.strip()
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sunplus.db")
    
    # JWT Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "d11ca7c6f09e66cd22026ae838234be19fde87cb9e47f2e185cde643c7b3be64")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    
    # Rate Limits
    RATE_LIMIT_PUBLIC_POST: str = os.getenv("RATE_LIMIT_PUBLIC_POST", "5/minute")
    RATE_LIMIT_PUBLIC_GET: str = os.getenv("RATE_LIMIT_PUBLIC_GET", "60/minute")
    
    # SMTP Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@sunpluspower.in")
    
    # Notifications
    NOTIFICATION_EMAIL_SALES: str = os.getenv("NOTIFICATION_EMAIL_SALES", "sales@sunpluspower.in")
    NOTIFICATION_EMAIL_ACCOUNTS: str = os.getenv("NOTIFICATION_EMAIL_ACCOUNTS", "accounts@sunpluspower.in")
    NOTIFICATION_EMAIL_SUPPORT: str = os.getenv("NOTIFICATION_EMAIL_SUPPORT", "support@sunpluspower.in")
    
    # Upload Constraints
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "5"))
    ALLOWED_IMAGE_EXTENSIONS: set = {
        ext.strip().lower() for ext in os.getenv("ALLOWED_IMAGE_EXTENSIONS", "jpg,jpeg,png").split(",") if ext.strip()
    }
    ALLOWED_DOCUMENT_EXTENSIONS: set = {
        ext.strip().lower() for ext in os.getenv("ALLOWED_DOCUMENT_EXTENSIONS", "pdf,doc,docx").split(",") if ext.strip()
    }
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")

settings = Settings()
