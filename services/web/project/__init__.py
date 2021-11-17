import os
import  json

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for,
    abort,
)

app = Flask(__name__)
app.config.from_object("project.config.Config")


@app.route("/")
def index():
    print("req /", flush=True)
    return "Hello"

@app.route("/static/<path:filename>")
def staticfiles(filename):
    print("req /static", flush=True)
    return send_from_directory(app.config["STATIC_FOLDER"], filename)

@app.route("/test/<username>")
def mediafiles(username):
    print("req /test", username, app.config["STATIC_FOLDER"], flush=True)
    #return "AAAAAAAAA"
    filename = username
    return send_from_directory(app.config["STATIC_FOLDER"], filename)
