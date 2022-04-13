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
  profile = read_token(request)
  footprint = {
    "start": data["start"],
    "end": data["stop"],
    "transport_mode": data["transport_mode"],
    "num_passengers": data["numPassengers"],
    "distance": footprintData["data"]["distance"]["miles"],
    "carbon_grams": str(int(footprintData["data"]["carbon_footprint"]["grams"]["total"])//int(data["numPassengers"])),
    "carbon_tons": str(int(footprintData["data"]["carbon_footprint"]["tons"]["total"])//int(data["numPassengers"])),
    "profile_id": profile["id"]
  }
  footprintDb = Footprint(**footprint)
  db.session.add(footprintDb)
  db.session.commit()
  return jsonify(footprint), 201

@footprints.route('/', methods=["GET"])
def index():
  footprints = Footprint.query.all()
  return jsonify([footprint.serialize() for footprint in footprints]), 201

@footprints.route('/delete/<id>', methods=["DELETE"])
@login_required
def delete(id):
  profile = read_token(request)
  footprint = Footprint.query.filter_by(id=id).first()
  
  if footprint.profile_id != profile["id"]:
    return 'Forbidden', 403
  
  db.session.delete(footprint)
  db.session.commit()
  return jsonify(message="Success"), 200

@footprints.route('/update/<id>', methods=["PUT"])
@login_required
def update(id):
  profile = read_token(request)
  data = request.get_json()
  print("data: ", data)
  print("id: ", id)
  start = data["start"]
  stop = data["stop"]
  transport_mode = data["transport_mode"]
  num_passengers = data["numPassengers"]
  url = f"https://klimaat.app/api/v1/calculate?start={start}&end={stop}&transport_mode={transport_mode}&num_passengers={num_passengers}{API_KEY}"
  footprintResponse = urllib.request.urlopen(url)
  footprintData = json.loads(footprintResponse.read())
  updatedFootprint = {
    "start": data["start"],
    "end": data["stop"],
    "transport_mode": data["transport_mode"],
    "num_passengers": data["numPassengers"],
    "distance": footprintData["data"]["distance"]["miles"],
    "carbon_grams": str(int(footprintData["data"]["carbon_footprint"]["grams"]["total"])//int(data["numPassengers"])),
    "carbon_tons": str(int(footprintData["data"]["carbon_footprint"]["tons"]["total"])//int(data["numPassengers"])),
    "profile_id": profile["id"]
  }
  footprint = Footprint.query.filter_by(id=id).first()
  footprint.start = data["start"]
  footprint.end = data["stop"]
  footprint.transport_mode = data["transport_mode"]
  footprint.num_passengers = data["numPassengers"]
  footprint.distance = footprintData["data"]["distance"]["miles"]
  footprint.carbon_grams = str(int(footprintData["data"]["carbon_footprint"]["grams"]["total"])//int(data["numPassengers"]))
  footprint.carbon_tons = str(int(footprintData["data"]["carbon_footprint"]["tons"]["total"])//int(data["numPassengers"]))
  footprint.profile_id = profile["id"]

  if updatedFootprint["profile_id"] != profile["id"]:
    return 'Forbidden', 403

  db.session.commit()
  return jsonify(updatedFootprint), 200
