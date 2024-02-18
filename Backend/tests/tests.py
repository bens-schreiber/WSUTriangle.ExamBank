import os
from pymongo import MongoClient
import pytest
from app import app, db, exam_collection

BLOB_IMAGE = "https://wsutriangle.blob.core.windows.net/exam-bank/Triangle Logo.jpeg"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_mongo(client):
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["test_database"]
    collection = db["test_collection"]
    collection.insert_one({"test_key": "test_value"})
    result = collection.find_one({"test_key": "test_value"})
    assert result is not None


def test_exam_post(client):
    json = {"name": "test", "tags": ["test"], "url": BLOB_IMAGE}
    response = client.post("/exam", json=json)

    assert response.status_code == 201
    assert response.data is not None

    post_identifier = response.data.decode('utf-8')

    # make sure its in the db
    result = exam_collection.find_one({"_id": str(post_identifier)})
    assert result is not None
