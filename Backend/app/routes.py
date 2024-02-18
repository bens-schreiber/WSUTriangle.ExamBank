from flask import Response, jsonify, request
from app import app, db, exam_collection
import uuid
from flasgger import swag_from


@swag_from(
    {
        "responses": {
            200: {"description": "Health check passed"},
        }
    }
)
@app.route("/health_check", methods=["GET"])
def health_check():
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

@swag_from(
    {
        "parameters": [
            {
                "in": "query",
                "name": "exam_id",
                "description": "The uuid of the exam to retrieve",
                "type": "string",
                "required": True,
            }
        ],
        "responses": {
            200: {
                "description": "Exam retrieved successfully",
                "content": {"application/json": {"schema": {"type": "object"}}},
            },
        },
    }
)
@app.route("/exam", methods=["GET"])
def get_exam():
    def validate_request(request):
        return "post_identifier" in request.json

    if not validate_request(request):
        return Response(status=400)

    post_identifier = request.json["post_identifier"]

    result = exam_collection.find_one({"_id": str(post_identifier)})
    result = result["data"]

    return Response(result, status=200)



@swag_from({
    "parameters": [
        {
            "name": "query",
            "in": "query",
            "type": "string",
            "required": True,
            "description": "The query string to search for exams."
        }
    ],
    "responses": {
        200: {
            "description": "A list of distinct exam results matching the query.",
            "schema": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "examples": {
                "result": ["Exam 1", "Exam 2"]
            }
        },
        400: {
            "description": "Bad request if the query parameter is missing."
        }
    }
})
@app.route("/exams/search", methods=["GET"])
def search_exam():
    def validate_request(request):
        return "query" in request.args

    if not validate_request(request):
        return Response(status=400)

    query = request.args["query"]
    distinct_results = exam_collection.find({"data": {"$regex": query}}).distinct(
        "data"
    )

    # Convert the result to a list of dictionaries
    result = [exam for exam in distinct_results]
    return jsonify(result), 200
