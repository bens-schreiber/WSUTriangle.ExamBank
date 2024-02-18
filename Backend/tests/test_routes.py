import os
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        

def test_Flask(client):
    response = client.get('/test123')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Hello, World!'}

def test_Swagger(client):
    response = client.get('/test')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == '"Hello, World!"\n'


