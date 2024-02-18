from flask import jsonify
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
