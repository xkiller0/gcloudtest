from flask import Flask, jsonify, request, render_template_string
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
import sqlite3

app = Flask(__name__)


@app.route("/api")
def redirect():
    return jsonify({"link": "https://www.bdtrckwz.com/KZDWFR/3M7TGPW/"})