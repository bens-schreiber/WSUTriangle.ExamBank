from flask import Flask
from flask_restx import Api
from pymongo import MongoClient
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
api = Api(app, version='1.0', title='GIF API',
          description='API for GIF backend')

client = MongoClient('mongodb://root:example@localhost:27017/')
# Connect to MongoDB
db = client['GIF-db']
from app import routes
