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


@app.route("/exam", methods=["POST", "GET"])
def exam():
    if request.method == "POST":
        data = request.json  
        exam_name = data.get("name")
        tags = data.get("tags", []) 
        pdf_url = data.get("pdf_url")

        if not (exam_name and pdf_url):
            return jsonify({"error": "Exam name and PDF URL are required"}), 400
        exam_doc = {
            "name": exam_name,
            "tags": tags,
            "pdf_url": pdf_url
        }
        try:
            db["exams"].insert_one(exam_doc)
            return jsonify({"message": "Exam data inserted successfully"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    