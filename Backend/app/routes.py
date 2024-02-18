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


@app.route('/exam',methods=["GET"])
def get_exam():
    def validate_request(request):
        return "post_identifier"  in request.json
    
    if not validate_request(request):
        print(request.json)
        return Response(status=400)
    
    post_identifier = request.json["post_identifier"]
    
    result = exam_collection.find_one({"_id": str(post_identifier)})
    result = result["data"]
    
    return Response(result,status=200)

@app.route('/exams/search',methods=["GET"])
def search_exam():
    def validate_request(request):
        return "query" in request.args
    
    if not validate_request(request):
        return Response(status=400)
    
    query = request.args["query"]
    distinct_results = exam_collection.find({ "data": { "$regex": query } }).distinct("data")

    # Convert the result to a list of dictionaries
    result = [exam for exam in distinct_results]
    return jsonify(result), 200

          
        
        
