import os
import uuid
from fastapi import HTTPException, UploadFile
from app.core.config import settings

class FileService:
    @staticmethod
    def save_file(file: UploadFile, allowed_types: str = "image") -> str:
        # Extract extension
        ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
        
        # Validate extensions
        if allowed_types == "image":
            if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image extension. Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
                )
        elif allowed_types == "document":
            if ext not in settings.ALLOWED_DOCUMENT_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid document extension. Allowed: {', '.join(settings.ALLOWED_DOCUMENT_EXTENSIONS)}"
                )
        else:
            raise HTTPException(status_code=400, detail="Invalid target file type specification.")
        
        # Determine file size
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)  # Reset pointer
        
        max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
            )
            
        # Ensure upload folder exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate clean unique filename
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Write to disk in chunks
        with open(filepath, "wb") as buffer:
            while chunk := file.file.read(1024 * 1024):  # 1MB chunks
                buffer.write(chunk)
                
        # Return Nginx-friendly relative URI
        return f"/uploads/{filename}"
