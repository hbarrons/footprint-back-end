from flask import Flask, Blueprint, jsonify, request
from api.middleware import login_required, read_token
import os
import urllib.request, json

from api.models.db import db
from api.models.footprint import Footprint

API_KEY = os.getenv('API_KEY')

footprints = Blueprint('footprints', 'footprints')

@footprints.route('/', methods=["POST"])
@login_required
def getFootprint():
  data = request.get_json()
  print("request data: ", data)
  # url = f"https://klimaat.app/api/v1/calculate?start=48208&end=90210&transport_mode=driving&num_passengers=1{API_KEY}"
  # print(url)
  # response = urllib.request.urlopen(url)
  # data = response.read()
  # print(data)
  # data = request.get_json()
  # profile = read_token(request)
  # data["profile_id"] = profile["id"]
  # footprint = Footprint(**data)
  # db.session.add(footprint)
  # db.session.commit()
  # return jsonify(footprint.serialize()), 201
