from flask import Flask
from pymongo import MongoClient
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app)
client = MongoClient('mongodb://root:example@localhost:27017/')
# Connect to MongoDB
db = client['backend']
exam_collection = db["exams"]
from app import routes




