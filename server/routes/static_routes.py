from flask import Blueprint, send_from_directory
import os

static_routes = Blueprint('static_routes', __name__)

@static_routes.route('/')
def index():
    return send_from_directory('../', 'index.html')

@static_routes.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../', path)
