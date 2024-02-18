from flask import Response, jsonify, request
from app import app, db, exam_collection
import uuid


@app.route("/flask_test", methods=["GET"])
def flask_test():
    return Response(status=200)


@app.route("/exam", methods=["POST"])
def post_exam():
    def validate_request(request):
        if "name" not in request.json:
            return False
        if "tags" not in request.json:
            return False
        if "url" not in request.json:
            return False
        return True

    if not validate_request(request):
        return Response(status=400)

    # make a uuid
    post_identifier = str(uuid.uuid4())
    insert_result = exam_collection.insert_one(
        {"_id": post_identifier, "data": str(request.json)}
    )
    assert insert_result.inserted_id is not None

    return Response(post_identifier, status=201)


