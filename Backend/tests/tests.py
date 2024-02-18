import os
from pymongo import MongoClient
import pytest
from app import app

BLOB_IMAGE = 'https://wsutriangle.blob.core.windows.net/exam-bank/Triangle Logo.jpeg'

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

def test_Mongo(client):
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["test_database"]
    collection = db["test_collection"]
    collection.insert_one({"test_key": "test_value"})
    result = collection.find_one({"test_key": "test_value"})
    assert result is not None


def test_exam_post(client):
    post = client.post(
        "/exam",
        data={
            "name": 'CALC3'
        },
    )
    assert response.status_code == 200
    assert response.get_data(as_text=True) == '"WORLD HELLO!"\n'

def test_examget(client):  



