from flask import Flask
from flask_restx import Api
from pymongo import MongoClient
app = Flask(__name__)
api = Api(app, version='1.0', title='EXAM API',
          description='API for Exam backend')

client = MongoClient('mongodb://root:example@localhost:27017/')

# Connect to MongoDB
db = client['backend']
exam_collection = db["exams"]
from app import routes



