from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.routers.auth import get_current_admin
from app.models.models import (
    AdminUser,
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
    LeadOut,
    LeadStatusUpdate,
    DistributorApplicationOut,
    DistributorApplicationStatusUpdate,
    WarrantyRegistrationOut,
    ComplaintOut,
    ComplaintStatusUpdate,
    ProjectCreate,
    ProjectOut,
    BlogCreate,
    BlogOut,
    EventCreate,
    EventOut,
    GalleryCreate,
    GalleryOut,
    CareerCreate,
    CareerOut,
    JobApplicationOut,
    DashboardStatsOut
)

router = APIRouter(prefix="/admin", dependencies=[Depends(get_current_admin)], tags=["Admin Management API"])

# Dashboard metrics
@router.get("/dashboard-stats", response_model=DashboardStatsOut)
def get_dashboard_stats(db: Session = Depends(get_db)):
    leads_count = db.query(Lead).count()
    dist_count = db.query(DistributorApplication).count()
    complaints_count = db.query(Complaint).count()
    projects_count = db.query(Project).count()
    careers_count = db.query(Career).filter(Career.is_active == True).count()
    
    return {
        "leads_count": leads_count,
        "distributor_applications_count": dist_count,
        "complaints_count": complaints_count,
        "projects_count": projects_count,
        "careers_count": careers_count
    }

# --- Submissions View Endpoints ---

@router.get("/leads", response_model=List[LeadOut])
def get_admin_leads(db: Session = Depends(get_db)):
    return db.query(Lead).order_by(Lead.created_at.desc()).all()

@router.patch("/leads/{id}/status", response_model=LeadOut)
def update_lead_status(id: int, payload: LeadStatusUpdate, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = payload.status
    db.commit()
    db.refresh(lead)
    return lead

@router.get("/distributor-applications", response_model=List[DistributorApplicationOut])
def get_admin_distributors(db: Session = Depends(get_db)):
    return db.query(DistributorApplication).order_by(DistributorApplication.created_at.desc()).all()

@router.patch("/distributor-applications/{id}/status", response_model=DistributorApplicationOut)
def update_distributor_status(id: int, payload: DistributorApplicationStatusUpdate, db: Session = Depends(get_db)):
    app = db.query(DistributorApplication).filter(DistributorApplication.id == id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    app.status = payload.status
    db.commit()
    db.refresh(app)
    return app

@router.get("/warranty-registrations", response_model=List[WarrantyRegistrationOut])
def get_admin_warranties(db: Session = Depends(get_db)):
    return db.query(WarrantyRegistration).order_by(WarrantyRegistration.created_at.desc()).all()

@router.get("/complaints", response_model=List[ComplaintOut])
def get_admin_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).order_by(Complaint.created_at.desc()).all()

@router.patch("/complaints/{id}/status", response_model=ComplaintOut)
def update_complaint_status(id: int, payload: ComplaintStatusUpdate, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Ticket not found")
    complaint.status = payload.status
    db.commit()
    db.refresh(complaint)
    return complaint

@router.get("/job-applications", response_model=List[JobApplicationOut])
def get_admin_job_applications(db: Session = Depends(get_db)):
    return db.query(JobApplication).order_by(JobApplication.created_at.desc()).all()


# --- CRUD operations for Projects ---

@router.get("/projects", response_model=List[ProjectOut])
def get_all_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

@router.post("/projects", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**payload.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.put("/projects/{id}", response_model=ProjectOut)
def update_project(id: int, payload: ProjectCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for key, val in payload.model_dump().items():
        setattr(project, key, val)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- CRUD operations for Blogs ---

@router.get("/blogs", response_model=List[BlogOut])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(Blog).order_by(Blog.created_at.desc()).all()

@router.post("/blogs", response_model=BlogOut, status_code=status.HTTP_201_CREATED)
def create_blog(payload: BlogCreate, db: Session = Depends(get_db)):
    # Check if slug unique
    existing = db.query(Blog).filter(Blog.slug == payload.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
        
    db_blog = Blog(**payload.model_dump())
    if db_blog.published:
        db_blog.published_at = datetime.now(timezone.utc)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

@router.put("/blogs/{id}", response_model=BlogOut)
def update_blog(id: int, payload: BlogCreate, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
        
    # Check slug unique if changed
    if payload.slug != blog.slug:
        existing = db.query(Blog).filter(Blog.slug == payload.slug).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug already exists")
            
    # Keep track of published state shifts
    was_published = blog.published
    for key, val in payload.model_dump().items():
        setattr(blog, key, val)
        
    if blog.published and not was_published:
        blog.published_at = datetime.now(timezone.utc)
    elif not blog.published:
        blog.published_at = None
        
    db.commit()
    db.refresh(blog)
    return blog

@router.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog post not found")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- CRUD operations for Events ---

@router.get("/events", response_model=List[EventOut])
def get_all_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.event_date.desc()).all()

@router.post("/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**payload.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/events/{id}", response_model=EventOut)
def update_event(id: int, payload: EventCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, val in payload.model_dump().items():
        setattr(event, key, val)
    db.commit()
    db.refresh(event)
    return event

@router.delete("/events/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- CRUD operations for Gallery ---

@router.get("/gallery", response_model=List[GalleryOut])
def get_all_gallery(db: Session = Depends(get_db)):
    return db.query(Gallery).order_by(Gallery.created_at.desc()).all()

@router.post("/gallery", response_model=GalleryOut, status_code=status.HTTP_201_CREATED)
def create_gallery_item(payload: GalleryCreate, db: Session = Depends(get_db)):
    db_gallery = Gallery(**payload.model_dump())
    db.add(db_gallery)
    db.commit()
    db.refresh(db_gallery)
    return db_gallery

@router.put("/gallery/{id}", response_model=GalleryOut)
def update_gallery_item(id: int, payload: GalleryCreate, db: Session = Depends(get_db)):
    item = db.query(Gallery).filter(Gallery.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    for key, val in payload.model_dump().items():
        setattr(item, key, val)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/gallery/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gallery_item(id: int, db: Session = Depends(get_db)):
    item = db.query(Gallery).filter(Gallery.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gallery item not found")
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- CRUD operations for Careers ---

@router.get("/careers", response_model=List[CareerOut])
def get_all_careers(db: Session = Depends(get_db)):
    return db.query(Career).order_by(Career.created_at.desc()).all()

@router.post("/careers", response_model=CareerOut, status_code=status.HTTP_201_CREATED)
def create_career(payload: CareerCreate, db: Session = Depends(get_db)):
    db_career = Career(**payload.model_dump())
    db.add(db_career)
    db.commit()
    db.refresh(db_career)
    return db_career

@router.put("/careers/{id}", response_model=CareerOut)
def update_career(id: int, payload: CareerCreate, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    for key, val in payload.model_dump().items():
        setattr(career, key, val)
    db.commit()
    db.refresh(career)
    return career

@router.delete("/careers/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_career(id: int, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.id == id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    db.delete(career)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
