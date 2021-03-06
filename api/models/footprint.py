from datetime import datetime
from api.models.db import db

class Footprint(db.Model):
    __tablename__ = 'footprints'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    transport_mode = db.Column(db.String(100))
    num_passengers = db.Column(db.Integer)
    distance = db.Column(db.Integer)
    carbon_grams = db.Column(db.String)
    carbon_tons = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
      return f"Footprint('{self.id}'"

    def serialize(self):
      footprint = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return footprint