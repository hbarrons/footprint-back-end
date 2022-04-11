from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from api.middleware import login_required, read_token
import os
import urllib.request, json

from api.models.db import db
from api.models.footprint import Footprint

API_KEY = os.getenv('API_KEY')

footprints = Blueprint('footprints', 'footprints')

@footprints.route('/', methods=["POST"])
@login_required
def createFootprint():
  data = request.get_json()
  print("data: ", data)
  start = data["start"]
  stop = data["stop"]
  transport_mode = data["transport_mode"]
  numPassengers = data["numPassengers"]
  # data.headers['Access-Control-Allow-Origin'] = '*'
  url = f"https://klimaat.app/api/v1/calculate?start={start}&end={stop}&transport_mode={transport_mode}&num_passengers={numPassengers}{API_KEY}"
  print(url)
  footprintResponse = urllib.request.urlopen(url)
  footprintData = footprintResponse.read()
  print(footprintData)
  profile = read_token(request)
  data["profile_id"] = profile["id"]
  # footprint = Footprint(**data)
  # db.session.add(footprint)
  # db.session.commit()
  # return jsonify(footprintData.serialize()), 201
