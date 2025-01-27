from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    entries = db.relationship('Entry', backref='vehicle', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    entry_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
