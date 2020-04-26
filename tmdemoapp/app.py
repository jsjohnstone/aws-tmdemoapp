# app.py
# aws-tmdemo app: a simple application for seeing upcoming 
# Ticketmaster events in New Zealand

from flask import Flask
from flask import render_template
import requests
import json
import os

TM_API_KEY = os.environ.get("TM_API_KEY")

app = Flask(__name__)             

@app.route("/")                  
def get_events():
    if not TM_API_KEY:
     return "No TM API KEY set for application"

    r = requests.get(
      'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=NZ&apikey=' + TM_API_KEY)
    data  = json.loads(r.text)

    return render_template('shows.html', title='Upcoming Shows', events=data['_embedded']['events']) 

if __name__ == "__main__":     
    app.run(host='0.0.0.0')               