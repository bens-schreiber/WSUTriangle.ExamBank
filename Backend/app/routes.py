from flask import jsonify
from flask_restx import Resource
from app import app, db
from pymongo.collection import Collection
from app import api

@api.route('/test', methods=['GET','POST'])
class Test(Resource):
    def get(self):
        return 'Hello, World!'
    def post(self):
        return 'WORLD HELLO!'
    
@app.route('/test123', methods=['GET'])
def test123():
    return jsonify({'message': 'Hello, World!'})


