# from .config import DATABASE_URL
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# initialize Flask app
app = Flask(__name__)
# CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
games_ref = db.collection('game_played')

from . import routes