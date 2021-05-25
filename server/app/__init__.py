# from .config import DATABASE_URL
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate


# initialize Flask app
app = Flask(__name__)
CORS(app)

from . import routes