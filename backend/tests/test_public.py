import pytest
from app.models.models import Project

def test_get_projects_portfolio_empty(client):
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []

def test_get_projects_portfolio_populated(client, db_session):
    # Seed a project
    from datetime import date
    new_proj = Project(
        name="Tech Campus Solar Layout",
        capacity_mw=1.2,
        location="Pune",
        state="Maharashtra",
        status="operational",
        commissioning_date=date(2025, 6, 15),
        image_url="https://images.unsplash.com/photo-1509391366360-2e959784a276",
        description="Rooftop crystalline arrays covering commercial campus layout."
    )
    db_session.add(new_proj)
    db_session.commit()

    response = client.get("/api/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Tech Campus Solar Layout"

def test_submit_general_contact_lead(client):
    payload = {
        "name": "Jane Miller",
        "email": "jane@industrial.com",
        "phone": "+91 9988776655",
        "company": "Miller Manufacturing",
        "subject": "500kW Solar Feasibility Inquiry",
        "message": "Interested in a 500kW rooftop installation feasibility report.",
        "source_page": "connect"
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == "Jane Miller"

def test_submit_distributor_partner_form(client):
    payload = {
        "company_name": "Apex Solar Distributors",
        "contact_person": "Ravi Kumar",
        "region": "Uttar Pradesh",
        "business_type": "distributor",
        "years_in_business": 8,
        "phone": "+91 9898989898",
        "email": "ravi@apexsolar.in",
        "message": "We have a network of 40 active installers across Lucknow, Kanpur, and Patna."
    }
    response = client.post("/api/distributor-applications", json=payload)
    assert response.status_code == 201
    assert response.json()["company_name"] == "Apex Solar Distributors"

def test_submit_invalid_phone_format(client):
    payload = {
        "name": "Jane Miller",
        "email": "jane@industrial.com",
        "phone": "invalid-phone",
        "subject": "Inquiry",
        "message": "Too short message",
        "source_page": "connect"
    }
    response = client.post("/api/leads", json=payload)
    assert response.status_code == 422
