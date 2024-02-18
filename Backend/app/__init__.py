from flask import Flask
from flask_restx import Api
from pymongo import MongoClient
from azure.storage.blob import BlockBlobService
from config import Config

app = Flask(__name__)
api = Api(app, version='1.0', title='EXAM API',
          description='API for Exam backend')

client = MongoClient('mongodb://root:example@localhost:27017/')

# Connect to MongoDB
db = client['backend']
exam_collection = db["exams"]
app.config.from_object(Config)

blob_service = BlockBlobService(account_name=app.config["AZURE_ACCOUNT"], account_key=app.config['AZURE_STORAGE_KEY'])

from app import routes



