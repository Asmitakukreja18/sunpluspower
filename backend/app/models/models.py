from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class TimestampMixin:
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        index=True, 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

class Lead(Base, TimestampMixin):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    company = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    source_page = Column(String(255), nullable=False)
    status = Column(String(50), default="new", index=True, nullable=False)  # new, contacted, closed

class CalculatorSubmission(Base, TimestampMixin):
    __tablename__ = "calculator_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    monthly_bill = Column(Float, nullable=False)
    monthly_units = Column(Float, nullable=False)
    location = Column(String(255), nullable=False)
    install_type = Column(String(100), nullable=False)  # rooftop, ground-mount
    calculated_system_size_kw = Column(Float, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    subsidy_amount = Column(Float, nullable=False)
    net_cost = Column(Float, nullable=False)
    annual_savings = Column(Float, nullable=False)
    payback_years = Column(Float, nullable=False)
    co2_offset_kg = Column(Float, nullable=False)

class DistributorApplication(Base, TimestampMixin):
    __tablename__ = "distributor_applications"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=False)
    region = Column(String(255), nullable=False)
    business_type = Column(String(255), nullable=False)
    years_in_business = Column(Integer, nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="pending", index=True, nullable=False)  # pending, approved, rejected

class WarrantyRegistration(Base, TimestampMixin):
    __tablename__ = "warranty_registrations"

    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String(255), nullable=False)
    serial_or_project_id = Column(String(255), nullable=False, index=True)
    installation_date = Column(Date, nullable=False)
    customer_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    installer_name = Column(String(255), nullable=False)

class Complaint(Base, TimestampMixin):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    project_or_product_id = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)  # installation, om, product, billing, other
    description = Column(Text, nullable=False)
    photo_url = Column(String(500), nullable=True)
    status = Column(String(50), default="open", index=True, nullable=False)  # open, in_progress, resolved

class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    capacity_mw = Column(Float, nullable=False)
    location = Column(String(255), nullable=False)
    state = Column(String(100), nullable=False, index=True)
    status = Column(String(100), nullable=False, index=True)  # operational, under_construction
    commissioning_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=False)

class Blog(Base, TimestampMixin):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    content = Column(Text, nullable=False)
    excerpt = Column(Text, nullable=False)
    cover_image_url = Column(String(500), nullable=False)
    author = Column(String(255), nullable=False)
    published = Column(Boolean, default=False, index=True, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)

class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    image_url = Column(String(500), nullable=False)

class Gallery(Base, TimestampMixin):
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    caption = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True)  # rooftop, ground-mount, om, infrastructure

class Career(Base, TimestampMixin):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    department = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    experience_required = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, index=True, nullable=False)

    applications = relationship("JobApplication", back_populates="career", cascade="all, delete-orphan")

class JobApplication(Base, TimestampMixin):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    resume_url = Column(String(500), nullable=False)
    cover_letter = Column(Text, nullable=True)

    career = relationship("Career", back_populates="applications")

class AdminUser(Base, TimestampMixin):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="admin", nullable=False)
