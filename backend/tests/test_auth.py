import pytest
from app.models.models import AdminUser
from app.core.security import get_password_hash

def test_admin_login_success(client, db_session):
    # Manually seed the test administrator account in SQLite memory
    hashed_pw = get_password_hash("SunPlusAdmin2026!")
    test_admin = AdminUser(
        email="admin@sunpluspower.in",
        hashed_password=hashed_pw,
        role="admin"
    )
    db_session.add(test_admin)
    db_session.commit()

    # Attempt authenticating
    login_payload = {
        "email": "admin@sunpluspower.in",
        "password": "SunPlusAdmin2026!"
    }
    response = client.post("/api/admin/login", json=login_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_admin_login_invalid_password(client, db_session):
    hashed_pw = get_password_hash("SunPlusAdmin2026!")
    test_admin = AdminUser(
        email="admin@sunpluspower.in",
        hashed_password=hashed_pw,
        role="admin"
    )
    db_session.add(test_admin)
    db_session.commit()

    login_payload = {
        "email": "admin@sunpluspower.in",
        "password": "WrongPassword!"
    }
    response = client.post("/api/admin/login", json=login_payload)
    assert response.status_code == 401

def test_unauthorized_dashboard_access(client):
    # Attempt loading admin leads data without authorization headers
    response = client.get("/api/admin/leads")
    assert response.status_code == 401
