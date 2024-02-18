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

    post_identifier = response.data.decode("utf-8")

    # make sure its in the db
    result = exam_collection.find_one({"_id": str(post_identifier)})
    assert result is not None


def test_exam_get(client):
    post_json = {"name": "test", "tags": ["test"], "url": BLOB_IMAGE}
    post_response = client.post("/exam", json=post_json)

    post_identifier = post_response.data.decode("utf-8")
    get_json = {"post_identifier": post_identifier}
    get_response = client.get("exam", json=get_json)

    assert get_response.status_code == 200
    assert str(post_json) == str(get_response.data.decode("utf-8"))


def test_exam_search(client):
    post_json = {
        "name": "An Elaborate Exam Name! 42",
        "tags": ["dog", "cat"],
        "url": BLOB_IMAGE,
    }
    client.post("/exam", json=post_json)

    def assert_search_response(response):
        assert response.status_code == 200
        data = eval(response.data.decode("utf-8"))
        print(data)
        assert data is not None
        assert len(data) > 0
        assert str(post_json) in data

    # We should be able to search for the exam by name
    search_response = client.get("/exams/search?query=An+Elaborate+Exam+Name!+42")
    assert_search_response(search_response)

    # We should be able to search for the exam by tag
    search_response_tag_1 = client.get("/exams/search?query=dog")
    search_response_tag_2 = client.get("/exams/search?query=cat")
    assert_search_response(search_response_tag_1)
    assert_search_response(search_response_tag_2)

    # We should be able to search with a partial query
    search_response_partial = client.get("/exams/search?query=Elaborate")
    assert_search_response(search_response_partial)

    # We should be able to search with a partial tag
    search_response_partial_tag = client.get("/exams/search?query=do")
    assert_search_response(search_response_partial_tag)




