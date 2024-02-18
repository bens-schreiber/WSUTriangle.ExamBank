from flask import Response, jsonify, request
from app import app, db, exam_collection, blob_service
import uuid


@app.route("/flask_test", methods=["GET"])
def flask_test():
    return Response(status=200)


@app.route("/exam", methods=["POST"])
def post_exam():
    def validate_request(request):
        if "file" not in request.files:
            return False
        if "name" not in request.form or "tags" not in request.form:
            return False

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


@app.route("/exams/search", methods=["GET"])
def search_exam():
    def validate_request(request):
        return "query" in request.args

    if not validate_request(request):
        return Response(status=400)

    query = request.args["query"]

    distinct_results = exam_collection.find({
        "$or": [
            {"data.name": {"$regex": query, "$options": 'i'}},
            {"data.tags": {"$regex": query, "$options": 'i'}}
        ]
    }).distinct("data")

    # Limit the results to the top 10
    distinct_results = distinct_results[:10]

    # Convert the result to a list of dictionaries
    result = [exam for exam in distinct_results]
    return jsonify(result), 200
