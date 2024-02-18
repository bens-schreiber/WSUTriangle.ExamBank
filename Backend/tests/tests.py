import os
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        

def test_flask(client):
    response = client.get('/flasktest')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Hello, World!'}

def test_swagger(client):
    response = client.get('/swaggertest')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == '"Hello, World!"\n'



