# app.py
# aws-tmdemo app: a simple application for seeing upcoming 
# Ticketmaster events in New Zealand

from flask import Flask
from flask import render_template
import requests
import json
import os

app = Flask(__name__)             
               
@app.route("/")
    def hello():
        return "Hello Blue!"

if __name__ == "__main__":     
    app.run(host='0.0.0.0')               