from app import db
from datetime import datetime

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Float, nullable=False)

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    quantity = db.Column(db.Float, default=1.0)

    food = db.relationship('Food')

