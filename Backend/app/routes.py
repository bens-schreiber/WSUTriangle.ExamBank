from flask import jsonify, request
from flask_restx import Resource
from app import app, db
from pymongo.collection import Collection
from app import api


@api.route("/swaggertest", methods=["GET", "POST"])
class Swaggertest(Resource):
    def get(self):
        return "Hello, World!"

    def post(self):
        return "WORLD HELLO!"


@app.route("/flasktest", methods=["GET"])
def flasktest():
    return jsonify({"message": "Hello, World!"})


@app.route("/exam", methods=["POST"])
def create_exam():
    if request.method == "POST":
        data = request.json
        exam_name = data.get("exam_name")
        tags = data.get("tags", [])
        pdf_url = data.get("pdf_url")
        if not (exam_name and pdf_url):
            return jsonify({"error": "Exam name and PDF URL are required"}), 400
        exam_doc = {"exam_name": exam_name, "tags": tags, "pdf_url": pdf_url}
        try:
            db["exams"].insert_one(exam_doc)
            return jsonify({"message": "Exam data inserted successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/exam", methods=["GET"])
def search_exams():
    if request.method == "GET":
        exam_name = request.args.get("exam_name")
        tags = request.args.getlist("tags")
        query = {}
        if exam_name:
            query["exam_name"] = exam_name
        if tags:
            query["tags"] = {"$in": tags}
        exams = db["exams"].find(query, {"_id": 0})
        return jsonify(list(exams)), 200
    return jsonify({"error": "Invalid request method"}), 405
