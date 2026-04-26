import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint returns 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_health_endpoint(client):
    """Test the health endpoint returns healthy"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_weather_without_city(client):
    """Test that missing city returns 400 error"""
    response = client.get('/weather')
    assert response.status_code == 400

def test_weather_with_city(client):
    """Test that a valid city returns 200"""
    response = client.get('/weather?city=London')
    assert response.status_code == 200