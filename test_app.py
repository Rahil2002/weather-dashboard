import pytest
from unittest.mock import patch, Mock
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
    """Test that a valid city returns 200 using a mocked API response"""

    # Fake the OpenWeatherMap API response
    # This way the test never makes a real API call
    # so it works even without the API key
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {
            "temp": 15.0,
            "feels_like": 13.0,
            "humidity": 80,
            "pressure": 1012
        },
        "wind": {"speed": 5.0},
        "weather": [{"main": "Clouds", "description": "overcast clouds"}]
    }

    # Patch the requests.get call inside app.py
    with patch('requests.get', return_value=mock_response):
        response = client.get('/weather?city=London')
        assert response.status_code == 200
        data = response.get_json()
        assert data['city'] == 'London'
        assert 'temperature' in data
        assert 'humidity' in data