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
  start = data["start"]
  stop = data["stop"]
  transport_mode = data["transport_mode"]
  num_passengers = data["numPassengers"]
  url = f"https://klimaat.app/api/v1/calculate?start={start}&end={stop}&transport_mode={transport_mode}&num_passengers={num_passengers}{API_KEY}"
  footprintResponse = urllib.request.urlopen(url)
  footprintData = json.loads(footprintResponse.read())
  print("footprintData: ", footprintData)
  profile = read_token(request)
  footprint = {
    "start": data["start"],
    "end": data["stop"],
    "transport_mode": data["transport_mode"],
    "num_passengers": data["numPassengers"],
    "distance": footprintData["data"]["distance"]["miles"],
    "carbon_grams": footprintData["data"]["carbon_footprint"]["grams"]["total"],
    "carbon_tons": footprintData["data"]["carbon_footprint"]["tons"]["total"],
    "profile_id": profile["id"]
  }
  print("footprint: ", footprint)
  footprintDb = Footprint(**footprint)
  db.session.add(footprintDb)
  db.session.commit()
  return jsonify(footprint.serialize()), 201
