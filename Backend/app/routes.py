from flask import Response, jsonify, request
from app import app, db, exam_collection, blob_service
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


@swag_from(
    {
        "summary": "Post a exam",
        "parameters": [
            {
                "name": "file",
                "in": "formData",
                "type": "file",
                "required": True,
                "description": "The exam to upload.",
            },
            {
                "name": "name",
                "in": "formData",
                "type": "string",
                "required": True,
                "description": "The name of the exam.",
            },
            {
                "name": "tags",
                "in": "formData",
                "description": "The tags of the exam.",
                "required": False,
                "type": "array",
                "items": {"type": "string"},
            },
        ],
        "responses": {
            201: {
                "description": "Exam successfully uploaded",
                "content": {"application/json": {"schema": {"type": "string"}}},
            },
            400: {"description": "Bad request if the file, name, or tags are missing."},
        },
    }
)
@app.route("/exam", methods=["POST"])
def post_exam():
    def validate_request(request):
        if "file" not in request.files:
            return False
        #  if "name" not in request.form or "tags" not in request.form:
        #      return False

        return True

    if not validate_request(request):
        return Response(status=400)

    # make a uuid
    post_identifier = str(uuid.uuid4())

    # file to be uploaded
    file = request.files["file"]
    file_name = f"{post_identifier}{file.filename}"
    container = app.config["AZURE_CONTAINER"]
    blob_service.create_blob_from_stream(container, file_name, file)

    # append url
    form_data = request.form.to_dict()
    form_data["url"] = (
        f"https://{app.config['AZURE_ACCOUNT']}.blob.core.windows.net/{container}/{file_name}"
    )

    exam_collection.insert_one({"_id": post_identifier, "data": form_data})

    return Response(post_identifier, status=201)


@swag_from(
    {
        "summary": "See a exam",
        "parameters": [
            {
                "name": "post_identifier",
                "in": "body",
                "schema": {
                    "type": "object",
                    "properties": {
                        "post_identifier": {
                            "type": "string",
                            "description": "The uuid of the exam to retrieve",
                        }
                    },
                },
            }
        ],
        "responses": {
            201: {
                "description": "Exam  successfully found",
                "content": {"application/json": {"schema": {"type": "string"}}},
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

    return jsonify(result), 200


@swag_from(
    {
        "parameters": [
            {
                "name": "query",
                "in": "query",
                "type": "string",
                "required": True,
                "description": "The query string to search for exams.",
            }
        ],
        "responses": {
            200: {
                "description": "A list of distinct exam results matching the query.",
                "schema": {"type": "array", "items": {"type": "string"}},
                "examples": {"result": ["Exam 1", "Exam 2"]},
            },
            400: {"description": "Bad request if the query parameter is missing."},
        },
    }
)
@app.route("/exams/search", methods=["GET"])
def search_exam():
    def validate_request(request):
        return "query" in request.args

    if not validate_request(request):
        return Response(status=400)

    query = request.args["query"]

    distinct_results = exam_collection.find(
        {
            "$or": [
                {"data.name": {"$regex": query, "$options": "i"}},
                {"data.tags": {"$regex": query, "$options": "i"}},
            ]
        }
    ).distinct("data")

    # Limit the results to the top 10
    distinct_results = distinct_results[:10]

    # Convert the result to a list of dictionaries
    result = [exam for exam in distinct_results]
    return jsonify(result), 200
