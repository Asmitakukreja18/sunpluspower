from datetime import datetime, timezone
import re
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, BackgroundTasks, status, Request
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.config import settings
from app.core.limiter import limiter
from app.services.email_service import email_service
from app.services.file_service import FileService
from app.models.models import (
    Lead,
    DistributorApplication,
    WarrantyRegistration,
    Complaint,
    Project,
    Blog,
    Event,
    Gallery,
    Career,
    JobApplication
)
from app.schemas.schemas import (
    LeadCreate,
    LeadOut,
    DistributorApplicationCreate,
    DistributorApplicationOut,
    WarrantyRegistrationCreate,
    WarrantyRegistrationOut,
    ComplaintOut,
    ProjectOut,
    BlogOut,
    EventOut,
    GalleryOut,
    CareerOut,
    JobApplicationOut
)

router = APIRouter(tags=["Public API Services"])

# Regex checks for Form inputs
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PHONE_REGEX = r"^(?:\+91|91|0)?[6-9]\d{9}$"

def validate_email_str(email: str) -> str:
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    return email

def validate_phone_str(phone: str) -> str:
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    if not re.match(PHONE_REGEX, cleaned):
        raise HTTPException(status_code=400, detail="Invalid Indian phone number format. Must be a 10-digit number.")
    return cleaned

@router.post("/leads", response_model=LeadOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PUBLIC_POST)
def submit_lead(
    request: Request,
    payload: LeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Save lead
    db_lead = Lead(**payload.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # Trigger background email notifications
    background_tasks.add_task(email_service.send_lead_notification, db_lead.__dict__)
    
    return db_lead

@router.post("/distributor-applications", response_model=DistributorApplicationOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PUBLIC_POST)
def submit_distributor(
    request: Request,
    payload: DistributorApplicationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_app = DistributorApplication(**payload.model_dump())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    
    background_tasks.add_task(email_service.send_distributor_notification, db_app.__dict__)
    
    return db_app

@router.post("/warranty-registrations", response_model=WarrantyRegistrationOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PUBLIC_POST)
def submit_warranty(
    request: Request,
    payload: WarrantyRegistrationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_warranty = WarrantyRegistration(**payload.model_dump())
    db.add(db_warranty)
    db.commit()
    db.refresh(db_warranty)
    
    # Format date string for email
    email_data = db_warranty.__dict__.copy()
    email_data["installation_date"] = db_warranty.installation_date.strftime("%Y-%m-%d")
    background_tasks.add_task(email_service.send_warranty_notification, email_data)
    
    return db_warranty

@router.post("/complaints", response_model=ComplaintOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PUBLIC_POST)
def submit_complaint(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    project_or_product_id: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Form validations
    email = validate_email_str(email)
    phone = validate_phone_str(phone)
    
    if category not in ["installation", "om", "product", "billing", "other"]:
        raise HTTPException(status_code=400, detail="Invalid complaint category.")
        
    photo_url = None
    if photo and photo.filename:
        photo_url = FileService.save_file(photo, allowed_types="image")
        
    db_complaint = Complaint(
        name=name,
        phone=phone,
        email=email,
        project_or_product_id=project_or_product_id,
        category=category,
        description=description,
        photo_url=photo_url
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    background_tasks.add_task(email_service.send_complaint_notification, db_complaint.__dict__)
    
    return db_complaint

@router.get("/projects", response_model=List[ProjectOut])
def list_projects(
    state: Optional[str] = None,
    status: Optional[str] = None,
    capacity_min: Optional[float] = None,
    capacity_max: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    if state:
        query = query.filter(Project.state.ilike(f"%{state}%"))
    if status:
        query = query.filter(Project.status == status)
    if capacity_min is not None:
        query = query.filter(Project.capacity_mw >= capacity_min)
    if capacity_max is not None:
        query = query.filter(Project.capacity_mw <= capacity_max)
        
    return query.order_by(Project.capacity_mw.desc()).all()

@router.get("/projects/{id}", response_model=ProjectOut)
def get_project(id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/blogs", response_model=List[BlogOut])
def list_blogs(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Only fetch published blogs
    skip = (page - 1) * limit
    blogs = db.query(Blog).filter(Blog.published == True).order_by(Blog.published_at.desc()).offset(skip).limit(limit).all()
    return blogs

@router.get("/blogs/{slug}", response_model=BlogOut)
def get_blog(slug: str, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.slug == slug, Blog.published == True).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog

@router.get("/events", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.event_date.desc()).all()

@router.get("/gallery", response_model=List[GalleryOut])
def list_gallery(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Gallery)
    if category:
        query = query.filter(Gallery.category == category)
    return query.order_by(Gallery.created_at.desc()).all()

@router.get("/careers", response_model=List[CareerOut])
def list_careers(db: Session = Depends(get_db)):
    return db.query(Career).filter(Career.is_active == True).order_by(Career.created_at.desc()).all()

@router.get("/careers/{id}", response_model=CareerOut)
def get_career(id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == id, Career.is_active == True).first()
    if not career:
        raise HTTPException(status_code=404, detail="Job opening not found")
    return career

@router.post("/careers/{id}/apply", response_model=JobApplicationOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PUBLIC_POST)
def apply_for_job(
    request: Request,
    id: int,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    cover_letter: Optional[str] = Form(None),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    email = validate_email_str(email)
    phone = validate_phone_str(phone)
    
    career = db.query(Career).filter(Career.id == id, Career.is_active == True).first()
    if not career:
        raise HTTPException(status_code=404, detail="Job opening not found")
        
    resume_url = FileService.save_file(resume, allowed_types="document")
    
    db_app = JobApplication(
        career_id=id,
        name=name,
        email=email,
        phone=phone,
        resume_url=resume_url,
        cover_letter=cover_letter
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    
    # HR email alert data
    email_data = db_app.__dict__.copy()
    email_data["job_title"] = career.title
    background_tasks.add_task(email_service.send_career_notification, email_data)
    
    return db_app

@router.post("/careers/apply-general", response_model=JobApplicationOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_PUBLIC_POST)
def apply_general(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    cover_letter: Optional[str] = Form(None),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    email = validate_email_str(email)
    phone = validate_phone_str(phone)
    
    resume_url = FileService.save_file(resume, allowed_types="document")
    
    db_app = JobApplication(
        career_id=None,
        name=name,
        email=email,
        phone=phone,
        resume_url=resume_url,
        cover_letter=cover_letter
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    
    email_data = db_app.__dict__.copy()
    email_data["job_title"] = "General Application"
    background_tasks.add_task(email_service.send_career_notification, email_data)
    
    return db_app
