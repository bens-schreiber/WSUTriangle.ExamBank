import io
from pymongo import MongoClient
import pytest
from app import app, exam_collection
from PIL import Image


def _json_test_image(name="test", tags=["test"]):
    """Returns a json object that can be used to post a test image to the server."""

    test_image = Image.new("RGB", (100, 100), (255, 0, 0))
    image_stream = io.BytesIO()
    test_image.save(image_stream, format="PNG")
    image_stream.seek(0)

    data = {
        "name": name,
        "tags": ",".join(tags),
        "file": (image_stream, f"{name}.jpeg"),
    }
    return data


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health_check")
    assert response.status_code == 200


def test_mongo(client):
    """Inserts a test document into the mongo database and then retrieves it."""

    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["test_database"]
    collection = db["test_collection"]
    collection.insert_one({"test_key": "test_value"})
    result = collection.find_one({"test_key": "test_value"})
    assert result is not None


def test_exam_post(client):
    """Posts a test image to the server and then checks that it is in the database."""

    post_json = _json_test_image()
    response = client.post("/exam", data=post_json)

    assert response.status_code == 201
    assert response.data is not None

    post_identifier = response.data.decode("utf-8")

    # make sure its in the db
    result = exam_collection.find_one({"_id": str(post_identifier)})
    assert result is not None


def test_exam_get(client):
    """Posts a test image to the server and then retrieves it."""

    post_json = _json_test_image()
    post_response = client.post("/exam", data=post_json)

    post_identifier = post_response.data.decode("utf-8")
    get_json = {"post_identifier": post_identifier}
    get_response = client.get("/exam", json=get_json)

    assert get_response.status_code == 200
    assert get_response.data is not None
    assert post_json["name"] in get_response.data.decode("utf-8")


def test_exam_search(client):
    """Posts a test image to the server and then searches for it in various ways."""

    post_json = _json_test_image("An Elaborate Exam Name! 42", ["dog", "cat"])
    client.post("/exam", data=post_json)

    def assert_search_response(response):
        assert response.status_code == 200
        data = eval(response.data.decode("utf-8"))
        assert data is not None
        assert len(data) > 0

        # make sure something in data is post_json
        found = False
        for exam in data:
            if post_json["name"] in exam["name"]:
                found = True
                break
        assert found

    # We should be able to search for the exam by name
    search_response = client.get("/exams/search?query=An Elaborate Exam Name! 42")
    assert_search_response(search_response)

    # We should be able to search for the exam by tag
    search_response_tag_1 = client.get("/exams/search?query=dog")
    search_response_tag_2 = client.get("/exams/search?query=cat")
    assert_search_response(search_response_tag_1)
    assert_search_response(search_response_tag_2)

    # # We should be able to search with a partial query
    search_response_partial = client.get("/exams/search?query=Elaborate")
    assert_search_response(search_response_partial)

    # # We should be able to search with a partial tag
    search_response_partial_tag = client.get("/exams/search?query=do")
    assert_search_response(search_response_partial_tag)
