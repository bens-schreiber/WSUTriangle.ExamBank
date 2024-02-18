from flask import Flask
from pymongo import MongoClient
from flasgger import Swagger
from azure.storage.blob import BlockBlobService
from config import Config

app = Flask(__name__)
swagger = Swagger(app)
client = MongoClient('mongodb://root:example@localhost:27017/')
# Connect to MongoDB
db = client['backend']
exam_collection = db["exams"]
app.config.from_object(Config)

blob_service = BlockBlobService(account_name=app.config["AZURE_ACCOUNT"], account_key=app.config['AZURE_STORAGE_KEY'])

from app import routes




