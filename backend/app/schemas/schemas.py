from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import re

# Helper regular expressions
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PHONE_REGEX = r"^(?:\+91|91|0)?[6-9]\d{9}$" # Indian 10-digit phone format

# Lead Schemas
class LeadBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: str
    phone: str
    company: Optional[str] = None
    subject: str = Field(..., min_length=2, max_length=255)
    message: str = Field(..., min_length=5)
    source_page: str = Field(..., max_length=255)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        # Stripping spaces and common characters
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(PHONE_REGEX, cleaned):
            raise ValueError("Invalid Indian phone number. Must be a 10-digit number.")
        return cleaned

class LeadCreate(LeadBase):
    pass

class LeadStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(new|contacted|closed)$")

class LeadOut(LeadBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Distributor Schemas
class DistributorApplicationCreate(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=255)
    contact_person: str = Field(..., min_length=2, max_length=255)
    region: str = Field(..., max_length=255)
    business_type: str = Field(..., max_length=255)
    years_in_business: int = Field(..., ge=0)
    phone: str
    email: str
    message: str = Field(..., min_length=5)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(PHONE_REGEX, cleaned):
            raise ValueError("Invalid Indian phone number")
        return cleaned

class DistributorApplicationStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|approved|rejected)$")

class DistributorApplicationOut(DistributorApplicationCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Warranty Schemas
class WarrantyRegistrationCreate(BaseModel):
    product_type: str = Field(..., max_length=255)
    serial_or_project_id: str = Field(..., max_length=255)
    installation_date: date
    customer_name: str = Field(..., min_length=2, max_length=255)
    phone: str
    email: str
    installer_name: str = Field(..., min_length=2, max_length=255)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(PHONE_REGEX, cleaned):
            raise ValueError("Invalid Indian phone number")
        return cleaned

class WarrantyRegistrationOut(WarrantyRegistrationCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Complaint Schemas
class ComplaintStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(open|in_progress|resolved)$")

class ComplaintOut(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    project_or_product_id: str
    category: str
    description: str
    photo_url: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Project Schemas
class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    capacity_mw: float = Field(..., gt=0)
    location: str = Field(..., max_length=255)
    state: str = Field(..., max_length=100)
    status: str = Field(..., pattern="^(operational|under_construction)$")
    commissioning_date: date
    description: str
    image_url: str = Field(..., max_length=500)

class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Blog Schemas
class BlogCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    slug: str = Field(..., min_length=2, max_length=255)
    content: str
    excerpt: str
    cover_image_url: str = Field(..., max_length=500)
    author: str = Field(..., max_length=255)
    published: bool = False

class BlogOut(BlogCreate):
    id: int
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Event Schemas
class EventCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: str
    event_date: date
    location: str = Field(..., max_length=255)
    image_url: str = Field(..., max_length=500)

class EventOut(EventCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Gallery Schemas
class GalleryCreate(BaseModel):
    image_url: str = Field(..., max_length=500)
    caption: str = Field(..., max_length=255)
    category: str = Field(..., pattern="^(rooftop|ground-mount|om|infrastructure)$")

class GalleryOut(GalleryCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Career Schemas
class CareerCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    department: str = Field(..., max_length=100)
    location: str = Field(..., max_length=100)
    experience_required: str = Field(..., max_length=100)
    description: str
    is_active: bool = True

class CareerOut(CareerCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Job Application Schemas
class JobApplicationOut(BaseModel):
    id: int
    career_id: Optional[int]
    name: str
    email: str
    phone: str
    resume_url: str
    cover_letter: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Admin Auth Schemas
class AdminLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AdminUserOut(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardStatsOut(BaseModel):
    leads_count: int
    distributor_applications_count: int
    complaints_count: int
    projects_count: int
    careers_count: int
