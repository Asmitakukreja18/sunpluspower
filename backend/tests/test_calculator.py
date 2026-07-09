import pytest

def test_calculator_basic_roi_endpoint(client):
    payload = {
        "name": "Ravi Shankar",
        "email": "ravi@gmail.com",
        "phone": "+91 9876543210",
        "monthly_bill": 8000,
        "monthly_units": 800,
        "location": "Uttar Pradesh",
        "install_type": "rooftop"
    }
    
    response = client.post("/api/calculator/submit", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "calculated_system_size_kw" in data
    assert "estimated_cost" in data
    assert "subsidy_amount" in data
    assert "payback_years" in data
    assert "net_cost" in data
    
    # Assert logical business outcomes
    assert data["calculated_system_size_kw"] > 0
    assert data["payback_years"] > 0

def test_calculator_validation_limits(client):
    # Invalid monthly bill bounds check
    payload = {
        "name": "Ravi Shankar",
        "email": "ravi@gmail.com",
        "monthly_bill": -50,
        "location": "Uttar Pradesh",
        "install_type": "rooftop"
    }
    response = client.post("/api/calculator/submit", json=payload)
    # Validation error expected
    assert response.status_code == 422
